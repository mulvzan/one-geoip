import os
import requests
import tarfile
import subprocess
import shutil

def download_singbox():
    """下载并解压sing-box工具"""
    try:
        # 创建临时目录
        os.makedirs("temp", exist_ok=True)
        
        # 固定使用Linux AMD64版本
        version = "1.11.5"
        url = f"https://github.com/SagerNet/sing-box/releases/download/v{version}/sing-box-{version}-linux-amd64.tar.gz"
        output_file = "temp/sing-box.tar.gz"
        
        print(f"正在下载sing-box: {url}")
        
        # 下载文件
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # 解压文件
        print("正在解压sing-box")
        with tarfile.open(output_file, 'r:gz') as tar:
            tar.extractall(path="temp")
        
        # 移动二进制文件
        binary_name = "sing-box"
        extracted_dir = "temp/sing-box-1.11.5-linux-amd64"
        shutil.copy(f"{extracted_dir}/{binary_name}", binary_name)
        
        # 修改权限使其可执行
        os.chmod(binary_name, 0o755)
        
        print(f"已准备好sing-box: {binary_name}")
        return binary_name
        
    except Exception as e:
        print(f"下载或解压sing-box时出错: {e}")
        return None

def compile_ruleset(binary_name):
    """使用sing-box编译规则集"""
    try:
        # 检查规则集JSON是否存在
        if not os.path.exists("one-china.json"):
            print("错误: one-china.json 文件不存在")
            return False
        if not os.path.exists("one-gfw.json"):
            print("错误: one-gfw.json 文件不存在")
            return False
        
        # 构建命令
        cmd1 = [f"./{binary_name}", "rule-set", "compile", "one-china.json"]
        cmd2 = [f"./{binary_name}", "rule-set", "compile", "one-gfw.json"]
        
        # 编译 one-china.json
        print(f"正在编译规则集: {' '.join(cmd1)}")
        result1 = subprocess.run(cmd1, capture_output=True, text=True)
        
        if result1.returncode != 0:
            print(f"编译 one-china.json 失败: {result1.stderr}")
            return False
        print(f"规则集编译成功: one-china.srs")

        # 编译 one-gfw.json
        print(f"正在编译规则集: {' '.join(cmd2)}")
        result2 = subprocess.run(cmd2, capture_output=True, text=True)

        if result2.returncode != 0:
            print(f"编译 one-gfw.json 失败: {result2.stderr}")
            return False
        print(f"规则集编译成功: one-gfw.srs")
        
        return True
        
    except Exception as e:
        print(f"编译规则集时出错: {e}")
        return False

def main():
    # 0. 清理工作目录，确保初始状态干净
    print("清理工作目录...")
    # 使用subprocess.run以更好地处理潜在的错误
    try:
        subprocess.run("git clean -fd", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"清理工作目录失败: {e}")
        return

    # 1. 下载IP和域名列表
    print("开始下载IP和域名列表...")
    subprocess.run(["python", "download_ip_lists.py"], check=True)
    
    # 2. 创建JSON规则集
    print("开始创建JSON规则集...")
    subprocess.run(["python", "create_ruleset.py"], check=True)

    # 下载sing-box
    binary_name = download_singbox()
    if not binary_name:
        return
    
    # 编译规则集
    if not compile_ruleset(binary_name):
        return

    # 4. 推送规则集
    print("开始推送规则集到rule-set分支...")
    subprocess.run(["python", "git_push_ruleset.py"], check=True)
    
    # 清理临时文件
    try:
        if os.path.exists("temp"):
            shutil.rmtree("temp")
        
        # 删除二进制文件
        # if os.path.exists(binary_name):
        #     os.remove(binary_name)
    except Exception as e:
        print(f"清理临时文件时出错: {e}")

if __name__ == "__main__":
    main()
