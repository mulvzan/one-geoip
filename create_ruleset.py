import json
import os

def create_ip_ruleset_json():
    """读取china.txt文件并创建sing-box IP规则集JSON文件"""
    try:
        # 检查china.txt是否存在
        if not os.path.exists("china.txt"):
            print("错误: china.txt 文件不存在")
            return False
        
        # 读取IP地址列表
        ip_cidrs = []
        with open("china.txt", 'r') as f:
            for line in f:
                # 去掉首尾空格
                line = line.strip()
                if line:
                    ip_cidrs.append(line)
        
        # 创建规则集JSON结构
        ruleset = {
            "version": 3,
            "rules": [
                {
                    "ip_cidr": ip_cidrs
                }
            ]
        }
        
        # 保存到文件
        with open("one-china.json", 'w') as f:
            json.dump(ruleset, f, indent=4)
        
        print(f"已创建IP规则集JSON文件: one-china.json，包含 {len(ip_cidrs)} 条IP规则")
        return True
    
    except Exception as e:
        print(f"创建IP规则集JSON时出错: {e}")
        return False

def create_domain_ruleset_json():
    """读取gfw.txt文件并创建sing-box域名规则集JSON文件"""
    gfw_file_path = "temp/gfw.txt"
    try:
        # 检查gfw.txt是否存在
        if not os.path.exists(gfw_file_path):
            print(f"错误: {gfw_file_path} 文件不存在")
            return False
        
        # 读取域名列表
        domains = []
        with open(gfw_file_path, 'r') as f:
            for line in f:
                # 去掉首尾空格和注释
                line = line.strip()
                if line and not line.startswith('#'):
                    domains.append(line)
        
        # 创建规则集JSON结构
        ruleset = {
            "version": 3,
            "rules": [
                {
                    "domain_suffix": domains
                }
            ]
        }
        
        # 保存到文件
        with open("one-gfw.json", 'w') as f:
            json.dump(ruleset, f, indent=4)
        
        print(f"已创建域名规则集JSON文件: one-gfw.json，包含 {len(domains)} 条域名规则")
        return True
    
    except Exception as e:
        print(f"创建域名规则集JSON时出错: {e}")
        return False

if __name__ == "__main__":
    create_ip_ruleset_json()
    create_domain_ruleset_json()