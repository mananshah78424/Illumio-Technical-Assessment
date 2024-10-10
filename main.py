import csv
import os


def create_lookup_map(file_path):
    lookup_map = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if row and len(row) >= 3:
                    dstport, protocol, tag = row
                    dstport = dstport.strip()
                    protocol = protocol.strip().lower() 
                    tag = tag.strip()
                    if dstport and protocol:
                        lookup_map[(dstport.lower(), protocol)] = tag  
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return lookup_map

def process_flow_logs(flow_log_file, lookup_table):
    tag_map = {}
    port_protocol_map = {}
    try:
        with open(flow_log_file, mode='r') as file:
            for line in file:
                fields = line.split()
                if len(fields) < 12:
                    continue
                
                dstport = fields[5].strip().lower()  
                protocol = fields[7]
                protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}

                protocol_name = protocol_map.get(protocol, 'unknown')

                tag = lookup_table.get((dstport, protocol_name.lower()), 'Untagged')  
                
                if tag not in tag_map:
                    tag_map[tag] = 0
                tag_map[tag] += 1
                
                if (dstport, protocol_name) not in port_protocol_map:
                    port_protocol_map[(dstport, protocol_name)] = 0
                port_protocol_map[(dstport, protocol_name)] += 1
        
    except FileNotFoundError:
        print(f"Error: The flow log file '{flow_log_file}' was not found.")
    except Exception as e:
        print(f"An error occurred while processing the flow logs: {e}")
        
    return tag_map, port_protocol_map

def write_output(tag_map, port_protocol_map, output_file):
    try:
        with open(output_file, mode='w') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag, count in tag_map.items():
                file.write(f"{tag},{count}\n")

            file.write("\nPort/Protocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in port_protocol_map.items():
                file.write(f"{port},{protocol},{count}\n")
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")

def main():
    lookup_csv = "lookup_csv.csv"
    flow_log_file = "flow_log_file.txt"
    output_file = "output.txt"

    lookup_map = create_lookup_map(lookup_csv)
    tag_map, port_protocol_map = process_flow_logs(flow_log_file, lookup_map)
    write_output(tag_map, port_protocol_map, output_file)
    
if __name__ == "__main__":
    main()
