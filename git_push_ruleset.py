import os
import subprocess
import time
from datetime import datetime

def run_command(command):
    """运行shell命令并返回结果"""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"命令执行失败: {command}")
            print(f"错误: {stderr}")
            return False
            
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def push_to_ruleset_branch(rule_files):
    """推送规则集文件到rule-set分支"""
    try:
        # 检查所有规则文件是否存在
        for file in rule_files:
            if not os.path.exists(file):
                print(f"错误: {file} 文件不存在")
                return False

        # 配置Git
        print("配置Git")
        if not run_command('git config --global user.name "GitHub Actions"'): return False
        if not run_command('git config --global user.email "actions@github.com"'): return False

        # 获取当前分支名，并切换到主分支 (main or master)
        main_branch = "main"
        if not run_command(f"git checkout {main_branch}"):
            main_branch = "master"
            if not run_command(f"git checkout {main_branch}"):
                print("错误: 无法切换到 'main' 或 'master' 分支。")
                return False
        print(f"已切换到主分支: {main_branch}")

        # 检查并删除远程的rule-set分支
        remote_branches = subprocess.check_output("git ls-remote --heads origin", shell=True).decode()
        if "refs/heads/rule-set" in remote_branches:
            print("正在删除远程的rule-set分支")
            if not run_command("git push origin --delete rule-set"): return False
            time.sleep(2)

        # 检查并删除本地的rule-set分支
        local_branches = subprocess.check_output("git branch", shell=True).decode()
        if "rule-set" in local_branches:
            print("正在删除本地的rule-set分支")
            if not run_command("git branch -D rule-set"): return False

        # 创建并切换到新的rule-set分支
        print("创建rule-set分支")
        if not run_command("git checkout --orphan rule-set"): return False

        # 清理工作区并添加规则文件
        if not run_command("git rm -rf --cached ."): return False
        print(f"添加规则文件: {', '.join(rule_files)}")
        for file in rule_files:
            if not run_command(f"git add -f {file}"): return False
        run_command("git add -f geosite-cn.srs")
        run_command("git add -f geosite-geolocation-!cn.srs")

        # 提交更改
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Update China IP and GFW domain rulesets - {current_time}"
        if not run_command(f'git commit -m "{commit_message}"'):
             # 即使没有更改也要继续，以支持空提交
            print("没有更改需要提交，或提交失败。继续推送...")

        # 推送到远程
        print("推送到远程rule-set分支")
        if not run_command("git push -u origin rule-set --force"): return False
                
        print("成功推送到rule-set分支")
        
        # 切换回主分支
        print(f"操作完成，切换回 {main_branch} 分支")
        run_command(f"git checkout {main_branch}")

        return True
        
    except Exception as e:
        print(f"推送到rule-set分支时出错: {e}")
        return False

if __name__ == "__main__":
    push_to_ruleset_branch(["one-china.srs", "one-gfw.srs"])