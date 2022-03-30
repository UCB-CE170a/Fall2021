import interface
from queue_model import Simulation, Node, Link
import pandas as pd
import numpy as np
from numba import jit

class Runner:
    def __init__(self, 
      links_csv: str, nodes_csv: str, od_csv: str,
      NodeClass=Node, LinkClass=Link):
        self.nodes_df = pd.read_csv(nodes_csv)
        self.links_df = pd.read_csv(links_csv)
        self.od_df = pd.read_csv(od_csv)
        self.sim = Simulation(NodeClass, LinkClass)

    def init_sq_simulation(self):
        self.sim.create_network(self.nodes_df, self.links_df)
        self.sim.create_demand(self.od_df)

        # remove vehicles from self.sim w/o path to the end
        cannot_find_path = []
        for vehicle_id, vehicle in self.sim.all_agents.items():
            routing_status = vehicle.get_path( g=self.sim.g )
            if routing_status == 'no_path_found':
                cannot_find_path.append(vehicle_id)

        [self.sim.all_agents.pop(vh_id) for vh_id in cannot_find_path]

        print(f'# o-d pairs whose paths cannot be found: {len(cannot_find_path)}')
        print(f'# o-d pairs/trips {len(self.sim.all_agents)}')
    
    def single_step_sq_sim(self, t):
        ### load agents
        for agent in self.sim.all_agents.values(): 
            agent.load_trips(t)
            ### reroute
            if t > 0 and t % self.reroute_freq == 0:
                agent.get_path( g=self.sim.g )
        ### run link model
        for link in self.sim.all_links.values():
            link.run_link_model(t)
        ### run node model
        node_ids_to_run = {link.end_nid for link in self.sim.all_links.values() if len(link.queue_veh) > 0}
        # for node_id in node_ids_to_run:
        #     node = self.sim.all_nodes[node_id] 
        #     node.run_node_model(t)

        @jit(nogil=True)
        def cmp_node_model():
            for nid in node_ids_to_run:
                node = self.sim.all_nodes[nid]
                node.run_node_model(t)
        
        cmp_node_model()



    # count the number of evacuees that have successfully reach their destination
    def arrival_counts(self, t,save_path):
        arrival_cnts = np.sum([1 for a in self.sim.all_agents.values() if a.status=='arr'])
        print(f'At {t} seconds, {arrival_cnts} evacuees successfully reached the destination')
        if arrival_cnts == len(self.sim.all_agents):
            print(f"all agents arrive at destinations at time {t} seconds.")
            return False
        with open(save_path, 'a') as t_stats_outfile:
            t_stats_outfile.write(f"{t},{arrival_cnts}\n")
        return True

    def write_link_outputs(self, save_path):
        link_output = pd.DataFrame([(link.lid, len(link.queue_veh), len(link.run_veh), np.round((len(link.queue_veh)+len(link.run_veh))/(link.length * link.lanes+0.00001)*100, 2), link.geometry) for link in self.sim.all_links.values() if link.ltype[0:2] != 'vl'], columns=['link_id', 'queue_vehicle_count', 'run_vehicle_count', 'vehicle_per_100m', 'geometry'])
        link_output = link_output[(link_output['queue_vehicle_count']>0) | (link_output['run_vehicle_count']>0)].reset_index(drop=True)
        link_output.to_csv(save_path, index=False)

    def spatial_queue_simulation(self, scenario_name, t_end=10801, output_dir='traffic_outputs'):
        arrival_output_path = f'{output_dir}/t_stats/arrivals_{scenario_name}.csv'
        with open(arrival_output_path, 'w') as t_stats_outfile:
            t_stats_outfile.write("t,arrival_count"+"\n")      

        # iterate through each time step
        for t in range(t_end):
            # run the spatial-queue simulation for one step
            self.single_step_sq_sim(t)

            # output time-step results every 100 seconds
            if t % 100 == 0 and self.arrival_counts(t, self.sim, arrival_output_path):                    
                link_output_path = f'{output_dir}/link_stats/l{scenario_name}_at_{t}.csv'
                node_output_path = f'{output_dir}/node_stats/n{scenario_name}_at_{t}.csv'
                self.write_link_outputs(self.sim, link_output_path)
                self.write_node_outputs(self.sim, node_output_path)
