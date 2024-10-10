# Flow Log Parser

This program parses a file containing flow log data and maps each row to a tag based on a lookup table defined in a CSV file. The program then generates an output file summarizing the counts of each tag and port/protocol combination. I have first created a lookup_map that acts as an hash map to store lookup_values.

## Logic

Use a search and lookup using a hash map. Made use of try except blocks for error handling.

## Assumptions

1. Flow Log Format:

   - The program only supports the default flow log format as specified in the AWS documentation. It is designed for version 2 logs only. I am assuming the flow logs are in a similar format and that we are most concerned with the dstport (field 5) and protocol (field 7).

2. CSV Format:

   - The lookup table CSV file must have a header row with the columns: "dstport", "protocol", "tag".
   - The "dstport" and "protocol" combinations are case insensitive.

3. Protocol Mapping: The program assumes the protocol field in the flow log data will use numeric values that map to their string equivalents:

   - "6" for "tcp"
   - "17" for "udp"
   - "1" for "icmp"
   - Any other value will be considered "unknown".
   - I have assumed we are dealing with only tcp, udp, and icmp. If we need more, we can easily add them to the map.
   - I have used https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml for finding the port numbers

4. Output File: The output file will contain:

   - A count of matches for each tag.
   - A count of matches for each port/protocol combination.
   - If a flow log entry does not match any tag in the lookup table, it will be counted as "Untagged".

5. Error Handling: The program skips any lines in the flow log file that do not have enough fields (fewer than 12) or if the required "dstport" and "protocol" cannot be extracted.

## Instructions

1. Requirements: Ensure you have Python installed on your machine.

2. Setup:

   - Clone this repository or download the files.
   - Place the flow log file (e.g., "flow_log_file.txt") and the lookup table CSV file (e.g., "lookup_csv.csv") in the same directory as the script.

3. Running the Program:

   - Open a terminal (or command prompt).
   - Navigate to the directory containing the script.
   - Run the program with the command: python main.py

4. Output: After running, check the directory for the "output.txt" file, which contains the results of the analysis.
