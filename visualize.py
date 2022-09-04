from scraper import get_followers, get_following, get_full_name_from_handle
from collections import defaultdict
from pyvis.network import Network
from random import choice, randint



MAX_DEPTH = 2                     # Maximum depth of the network
take_followers = True             # Whether to consider followers or not in the network
take_following = True             # Whether to consider following or not in the network




root_node = ""
full_name = {}
network = defaultdict(list)
visited = set()
colors = ['#808080', '#FF0000', '#800000', '#FFFF00', '#808000', '#00FF00', '#008000', '#00FFFF', '#008080', '#0000FF', '#000080', '#FF00FF', '#800080']
# colors = ['#ff4000', '#ff8000', '#ffbf00', '#ffff00', '#bfff00', '#80ff00', ' #40ff0', ' #00ff0', ' #00ff4', ' #00ff8', ' #00ffb', ' #00fff', ' #00bff', ' #0080f', ' #0040f', ' #0000f', ' #4000f', ' #8000f', ' #bf00f', ' #ff00f', ' #ff00b', ' #ff008', ' #ff004', ' #ff000']
root_color = '#ff0000'   # Red

def dfs(handle, level=0, take_followers=True, take_following=True):
    # visited.add(handle)
    if level > MAX_DEPTH:
        return

    print(level, handle)

    if take_followers:
        for follower, name in get_followers(handle):
            if follower not in visited:
                if follower not in network[handle]: network[handle].append(follower)
                if handle not in network[follower]: network[follower].append(handle)
                full_name[follower] = name
                dfs(follower, level+1, take_followers, take_following)
    
    if take_following:
        for following, name in get_following(handle):
            if following not in visited:
                if following not in network[handle]: network[handle].append(following)
                if handle not in network[following]: network[following].append(handle)
                full_name[following] = name
                dfs(following, level+1, take_followers, take_following)


def bfs(handle, take_followers=True, take_following=True):
    queue = [(handle, 0)]
    while queue:
        handle, level = queue.pop(0)
        if level >= MAX_DEPTH:
            return

        print(f"{level:^10}{handle:^30}")

        if take_followers:
            for follower, name in get_followers(handle):
                if follower not in full_name:
                    if follower not in network[handle]: network[handle].append(follower)
                    if handle not in network[follower]: network[follower].append(handle)
                    full_name[follower] = name
                    queue.append((follower, level+1))
        
        if take_following:
            for following, name in get_following(handle):
                if following not in full_name:
                    if following not in network[handle]: network[handle].append(following)
                    if handle not in network[following]: network[following].append(handle)
                    full_name[following] = name
                    queue.append((following, level+1))


if __name__ == "__main__":

    # Taking input
    root_node = input("Enter your GitHub handle: ").strip()
    take_following = False if "n" in input("Do you want to consider your GitHub following in the network? (y/n): ").strip().lower() else True
    take_followers = False if "n" in input("Do you want to consider your GitHub followers in the network? (y/n): ").strip().lower() else True

    print(f"{'Depth':^10}{'Handle':^30}")
    print(f"{'=====':^10}{'======':^30}")
    bfs(root_node, take_following=take_following, take_followers=take_followers)
    print()
    print("Network built")

    full_name[root_node] = get_full_name_from_handle(root_node)
    net = Network()

    titles, values, labels, cols = [], [], [], []
    node_ids = list(range(1, len(full_name)+1))
    get_node_id = dict(zip(full_name.keys(), node_ids))
    print(get_node_id)
    for handle in full_name:
        titles.append(handle)
        cols.append(choice(colors))
        # cols.append("%03x" % randint(0, 0xFFF))
        values.append(max(3 * len(network[handle]), 10))
        labels.append(full_name[handle] if full_name[handle] else handle)
        if handle == root_node:
            values[-1] = 150
            cols[-1] = root_color

    net.add_nodes(node_ids, value=values, title=titles, label=labels, color=cols)

    for u in network:
        for v in network[u]:
            # print(u, v)
            net.add_edge(get_node_id[u], get_node_id[v])
    
    net.write_html('output.html')
    net.show('output.html')
    print("\nOutput written to output.html")