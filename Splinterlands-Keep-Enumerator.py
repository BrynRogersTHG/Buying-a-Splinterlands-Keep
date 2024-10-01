# Buying a Splinterlands Keep enumurator.
# v.1.0
#
# Run this before you buy, the script is a base, it's unfinished.
#
# @slobberchops (HIVE account, @brynrogers)

import requests
import os

class bcolors:
     HEADER = '\033[95m'
     BLUE = '\033[94m'
     CYAN = '\033[96m'
     GREEN = '\033[92m'
     YELLOW = '\033[93m'
     VIOLET = '\033[35m'
     RED = '\033[91m'
     END = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'

os.system("")

# ==============================================================================================================================

def fetch_yield_data(UID, region_UID, plot, total_grain_yield, total_shard_yield, total_research_yield, worksite_type):
    url = f"https://vapi.splinterlands.com/land/stake/deeds/{UID}/assets"
    response = requests.get(url)
    
    data = response.json()
    monsters = data.get('data', {}).get('cards', [])
    total_production_per_hour = 0
    
    for monster in monsters:
        production_per_hour = float(monster.get('work_per_hour', 0))
        total_production_per_hour += production_per_hour
    
    if worksite_type == "Grain Farm":
        print(bcolors.GREEN + f" {region_UID}-{plot} (GRAIN - Combined Production Per Hour: {total_production_per_hour})" + bcolors.END)
        total_grain_yield += total_production_per_hour
    elif worksite_type == "Shard Mine":
        print(bcolors.RED + f" {region_UID}-{plot} (SHARD MINE - Combined SPS Per Hour: {total_production_per_hour})" + bcolors.END)
        total_shard_yield += total_production_per_hour
    elif worksite_type == "Research Hut":
        print(bcolors.CYAN + f" {region_UID}-{plot} (RESEARCH - Combined Research Per Hour: {total_production_per_hour})" + bcolors.END)
        total_research_yield += total_production_per_hour

    return total_grain_yield, total_shard_yield, total_research_yield

# ==============================================================================================================================

def get_land_deeds_in_range(start_id, end_id, filename, region, tract, total_grain_yield, total_shard_yield, total_research_yield):
    null_worksite_count = 0 
    cleared_but_not_used = 0
    total_idle_land = 0
    plot = "001"
    print (f"Region - {region}, Tract - {tract}")
    print ("---------------------------------------------------")

    with open(filename, 'w') as file:
        for deed_id in range(start_id, end_id + 1):
            url = f"https://vapi.splinterlands.com/land/deeds/{deed_id}"
            response = requests.get(url)

            deed_data = response.json().get('data', {})
            region_uid = deed_data.get('region_uid')
            player = deed_data.get('player')
            worksite_type = deed_data.get('worksite_type')
            listed = deed_data.get('listed')
            listing_price = deed_data.get('listing_price')
            in_use = deed_data.get('in_use')
            UIDData = deed_data.get('deed_uid')
            output_line = ""

            if listed:
                output_line += f" | Listed: Yes | Listing Price: ${listing_price}"
            else:
                output_line += " | Listed: No"

            if worksite_type != "" and in_use == False:
                cleared_but_not_used += 1

            if worksite_type == "":
                null_worksite_count += 1
                output_line += " | Worksite Type: Not Cleared"
                worksite_type = "Not Cleared"

            output_line = f"Plot: {region_uid}-{plot}  | Player: {player} | Type: {worksite_type} | Used: {in_use}"

            total_grain_yield, total_shard_yield, total_research_yield = fetch_yield_data(UIDData, region_uid, plot, total_grain_yield, total_shard_yield, total_research_yield, worksite_type)

            file.write(output_line + "\n")
            print(output_line)
            
            plot = str(int(plot) + 1).zfill(3)

        total_idle_land = null_worksite_count + cleared_but_not_used
        final_output = f"\n  Region: {region} Tract: {tract}\n Uncleared Land: {null_worksite_count}\n Cleared, but Not Used: {cleared_but_not_used}\n Total, Idle Land: {total_idle_land}\n Grain Per Hour for Tract: {total_grain_yield}\n SPS Per Hour for Tract: {total_shard_yield}\n Research Per Hour for Tract: {total_research_yield}"
        file.write(final_output)
        print(final_output)

if __name__ == "__main__":
    
    total_grain_yield = 0
    total_shard_yield = 0
    total_research_yield = 0

    # Add your own data below, comment in and out to swap.

    #start_id = 77101
    #end_id = 77200
    #region = "Celestine"
    #tract = "06"

    # region = "Val De Lun"
    # tract = "07"
    # start_id = 96801
    # end_id = 96900

    #region = "Osburg"
    #tract = "03"
    #start_id = 30601
    #end_id = 30700

    #region = "Viritas"
    #tract = "04"
    #start_id = 45001
    #end_id = 45100

    #region = "Harkden"
    #tract = "10"
    #start_id = 136301
    #end_id = 136400

    region = "Briarwood"
    tract = "3"
    start_id = 32701
    end_id = 32800

    filename = "plotdata.txt"
    os.system('cls')

    get_land_deeds_in_range(start_id, end_id, filename, region, tract, total_grain_yield, total_shard_yield, total_research_yield)
