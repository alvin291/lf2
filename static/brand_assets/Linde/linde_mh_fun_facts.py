import random

# List of fun facts about Linde Material Handling (Linde MH)
linde_mh_facts = [
    "Linde Material Handling, part of the KION Group, has been a global leader in forklift trucks and warehouse equipment since its founding in 1904, pioneering innovations for over a century!",
    "Linde MH introduced the world’s first hydrostatic transmission for forklifts in the 1960s, revolutionizing efficiency and precision in material handling.",
    "With a rental fleet of over 60,000 trucks worldwide, Linde MH ensures businesses can access top-quality forklifts on demand, keeping warehouses moving smoothly.",[](https://www.linde-mh.com/en/)
    "Linde MH’s Zero Accident Philosophy drives their mission to make intralogistics safer, integrating advanced safety solutions for people, trucks, and goods.",[](https://www.linde-mh.com/en/)
    "Linde MH is a pioneer in sustainability, partnering with Li-Cycle to recycle up to 95% of lithium-ion batteries used in their electric forklifts, reducing environmental impact.",[](https://finance.yahoo.com/news/li-cycle-kion-group-form-100000303.html)
    "The KION Group, Linde MH’s parent company, adopted the motto ‘We keep the world moving,’ reflecting their commitment to global supply chain solutions, even during crises like the pandemic.",[](https://www.linde-mh.com/en/About-us/Magazine/crucial-role-within-the-system.html#:~:text=Linde%20Material%20Handling%20and%20the%20KION%20Group%20keep%20the%20material%20flow%20running&text=%27We%20keep%20the%20world%20moving%2Cparent%20company%2C%20the%20KION%20Group.)
    "Linde MH’s ergonomic design philosophy ensures their trucks and services prioritize operator comfort, boosting productivity and reducing fatigue in warehouses.",[](https://www.linde-mh.com/en/)
    "Linde MH is a leader in telematics, with hundreds of thousands of their forklifts equipped with advanced systems to optimize fleet management and performance.",[](https://finance.yahoo.com/news/global-material-handling-equipment-telematics-144500652.html)
    "Since joining the KION Group in 2006, Linde MH has expanded its global reach, becoming the market leader in Europe for forklift trucks and warehouse equipment.",[](https://linde-mh.com.my/company/)
    "Linde MH’s ‘Smart Factory’ in Stříbro, Czech Republic, uses digitally networked systems to produce up to 12,000 industrial trucks annually, showcasing cutting-edge manufacturing."[](https://warehousenews.co.uk/2016/04/sabine-neuss-to-lead-linde-for-another-four-years/)
]

# Function to display a random fun fact
def display_random_fact():
    fact = random.choice(linde_mh_facts)
    print("Fun Fact about Linde Material Handling:")
    print(fact)

# Run the function
if __name__ == "__main__":
    display_random_fact()