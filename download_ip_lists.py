import os
import requests

def download_file(url, output_file):
    """下载文件并保存到指定路径"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"成功下载: {url} -> {output_file}")
        return True
    except Exception as e:
        print(f"下载失败: {url}, 错误: {e}")
        return False

def main():
    # 创建临时目录
    os.makedirs("temp", exist_ok=True)
    
    # 下载IPv4列表
    ipv4_url = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china.txt"
    gfw_url = "https://github.com/Loyalsoldier/v2ray-rules-dat/raw/refs/heads/release/gfw.txt"
    ipv4_file = "temp/china.txt"
    gfw_file = "temp/gfw.txt"
    output_file = "china.txt"
    
    # 下载文件
    download_file(ipv4_url, ipv4_file)
    download_file(gfw_url, gfw_file)
    # 合并文件
    with open(output_file, 'w') as outfile:
        for infile in [ipv4_file]:
            try:
                with open(infile, 'r') as f:
                    for line in f:
                        # 去掉首尾空格
                        cleaned_line = line.strip()
                        if cleaned_line:
                            outfile.write(f"{cleaned_line}\n")
            except Exception as e:
                print(f"处理文件 {infile} 时出错: {e}")
    
    print(f"已合并IP列表到 {output_file}")

if __name__ == "__main__":
    main()
