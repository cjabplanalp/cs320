from collections import deque
import os
import pandas as pd
import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        return self.dfs_visit(node)
                                          
    def dfs_visit(self, node):
        if node in self.visited:
            return
        
        self.visited.add(node)
        self.order.append(node)
        
        children = self.go(node)
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        
        todo = deque([node])
        self.order = [node]
        
        while len(todo) > 0:
            curr_node = todo.popleft()
            
            for child in self.go(curr_node):
                if not child in self.order:
                    todo.append(child)
                    self.order.append(child)    
        return None
                    
                
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def go(self, node):
        children = []
        for child, edge in self.df.loc[node].items():
            if edge == 1:
                children.append(child)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        self.output_message = []

    def go(self, file):
        all_lines = []
        
        if file in os.listdir("file_nodes"):
            path = os.path.join("file_nodes", file)
            f = open(path, "r")
            contents = f.readlines()
            
            for lines in contents:
                if lines != "\n":
                    all_lines.append(lines.strip().split(","))
        
        self.output_message.append(''.join(all_lines[0]))
        
        return all_lines[1]
    
    def message(self):
        return ''.join(self.output_message)

class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.dfs = []
        
    def go(self, url):
        children = []
        
        self.driver.get(url)
        links = self.driver.find_elements(by = "tag name", value = "a")
        for child in links:
            children.append(child.get_attribute("href"))
        
        self.dfs.append(pd.read_html(self.driver.page_source)[0])
        
        return children
    
    def table(self):
        return pd.concat(self.dfs, ignore_index = True)
    
def reveal_secrets(driver, url, travellog):
    #step1
    nums = []
    for number in travellog['clue']:
        nums.append(str(number))
    password = ''.join(nums)
    
    #step2
    driver.get(url)
    
    #step3
    driver.find_element(by = "id", value = "password").send_keys(password)
    driver.find_element(by = "id", value = "attempt-button").click()
    
    #step4
    time.sleep(1)
    
    #step5
    driver.find_element(by = "id", value = "securityBtn").click()
    time.sleep(2)
    
    #step6
    img_url = driver.find_element(by = "id", value = "image").get_attribute("src")
    
    # cited from https://www.adamsmith.haus/python/answers/how-to-download-an-image-using-requests-in-python#:~:text=Use%20requests.,write%2Dand%2Dbinary%20mode
    response = requests.get(img_url)
    file = open("Current_Location.jpg", "wb")
    file.write(response.content)
    file.close()
    
    #step7
    return driver.find_element(value = "location").text
    
    