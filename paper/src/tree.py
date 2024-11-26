import pygeohash as pgh
import tqdm

def geohash_approximate_distance(geohash1: str, geohash2: str) -> int:
    return pgh.geohash_approximate_distance(geohash1, geohash2)

class GeoHashTreeNode:
    def __init__(self):
        self.children = {}

class GeoHashTree:
    def __init__(self):
        self.root = GeoHashTreeNode()

    def insert(self, geohash):
        current_node = self.root
        for char in geohash:
            if char not in current_node.children:
                current_node.children[char] = GeoHashTreeNode()
            current_node = current_node.children[char]

    def query(self, geohash_prefix):
        current_node = self.root
        for char in geohash_prefix:
            if char not in current_node.children:
                return set()  # No matches found
            current_node = current_node.children[char]
        
        # Collect all geohashes under the prefix
        results = set()
        self.collect_geohashes(current_node, geohash_prefix, results)
        return results

    def collect_geohashes(self, node, prefix, results):
        if not node.children:
            results.add(prefix)
            return
        for char, child in node.children.items():
            self.collect_geohashes(child, prefix + char, results)
    # 新增的返回树拓扑结构（每层分支数）的方法
    def get_tree_topology(self):
        topology = []
        self._get_tree_topology_helper(self.root, 0, topology)
        return topology

    def _get_tree_topology_helper(self, node, level, topology):
        if len(topology) <= level:
            topology.append(0)
        topology[level] += len(node.children)  # 记录当前层的分支数

        for child in node.children.values():
            self._get_tree_topology_helper(child, level + 1, topology)
    # 新增：计算每一层的分支和过滤效果
    def get_tree_topology_with_filter(self):
        topology = []
        filter_effect = []
        self._get_tree_topology_with_filter_helper(self.root, 0, topology, filter_effect)
        return topology, filter_effect

    def _get_tree_topology_with_filter_helper(self, node, level, topology, filter_effect):
        if len(topology) <= level:
            topology.append(0)
            filter_effect.append([])  # 初始化过滤效果
        
        num_children = len(node.children)
        topology[level] += num_children  # 记录当前层的分支数
        
        # 计算当前节点的过滤效果
        filtered = 0
        for char, child in node.children.items():
            child.filtered_count = num_children - 1  # 当前节点的每个子节点过滤掉了其他分支
            filtered += child.filtered_count
        
        # 记录该层每个分支的过滤效果
        filter_effect[level].append(filtered)

        # 递归处理子节点
        for child in node.children.values():
            self._get_tree_topology_with_filter_helper(child, level + 1, topology, filter_effect)


        

def greedy_search(geohash, tree):
    current_geohash = geohash
    while current_geohash:
        results = tree.query(current_geohash)
        if results:
            return results
        current_geohash = current_geohash[:-1]  # Reduce geohash length by 1
    return set()  # No matches found for any geohash length

# 遍历所有的geohash，找到最近的geohash
def find_nearest_geohash(geohash, geohashes):
    min_distance = float('inf')
    nearest_geohash = None
    for gh in geohashes:
        distance = geohash_approximate_distance(geohash, gh)
        if distance < min_distance:
            min_distance = distance
            nearest_geohash = gh
    return nearest_geohash

def create_geohash_tree(geohashes):
    geohash_tree = GeoHashTree()
    print("Inserting geohashes into the tree...")
    for geohash in tqdm.tqdm(geohashes):
        geohash_tree.insert(geohash)
    return geohash_tree 

# Example usage:
# Create a GeoHashTree
geohash_tree = GeoHashTree()

# Insert geohashes into the tree
geohashes = [
'wtw1m8bb7hyc',
'wtw1m4yxrbd8',
'wtw1kcmjm24u',
'wtw1jyfnhgcs',
'wtw1tkyb1fwc',
'wtw1mm9dtvh0',
'wtw332dqvyep',
'wtw2cycwpbrv',
'wtw1xbg7qyjn',
'wtw23m94mk3x',
'wtw29jqvdzsj',
'wtw2dtxvhjnm',
'wtw2f9vkfcrj',
'wtw1xwfmq12x',
'wtw30fdddwvf',
'wtw0yycg8pjv',
'wtw0xrhd3x38',
'wtw6nf1bj7pw',
'wtw380nmd0cj',
]  # List of geohashes

for geohash in geohashes:
    geohash_tree.insert(geohash)



# # Query nearby geohashes for a given geohash prefix
# geohash_prefix = "wtw6jkguctxb"

# # 打印最近的geohash
# results = greedy_search(geohash_prefix, geohash_tree)
# nearest_geohash = find_nearest_geohash(geohash_prefix, results)

# # 取 results 中的第一个元素
# print("Nearby geohashes:", results.pop())
# print("Nearest geohash:", nearest_geohash)