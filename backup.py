
from requests.auth import HTTPBasicAuth
import requests
import urllib.parse
import json
import base64
import os
import logging
from datetime import date
import shutil
import stat


org_name = "ur org_name"
pat = "ur pat"
backup_folder = "backup"


org_name = urllib.parse.quote(org_name)
pat_bytes = (':'+pat).encode('ascii')
base64_bytes = base64.b64encode(pat_bytes).decode('utf-8')
B64_PAT=base64_bytes
today = date.today()
today_str = today.strftime("%Y-%m-%d")


def init_logging():

    fn = os.path.join('.','logs',f'{today_str}.log')
    logging.basicConfig(filename=fn,  level=logging.DEBUG)

def get_prj_list(org_name,pat):
    url = f'https://dev.azure.com/{org_name}/_apis/projects?api-version=6.0'
    
    logging.info(f'get_prj_list:{url}')
    
    response = requests.get(url, auth=HTTPBasicAuth('', pat))
    
    logging.info(f'get_prj_list:{response.status_code}')

    if(response.status_code == 200):
        return json.loads(response.text)

    return None

def get_git_repo_list_from_prj(org_name,prj_name,pat):
    
    logging.info(f'get_git_repo_list_from_prj:{prj_name}')
    url = f'https://dev.azure.com/{org_name}/{prj_name}/_apis/git/repositories?includeLinks=True&api-version=6.0'

    logging.info(f'get_git_repo_list_from_prj:{url}')

    response = requests.get(url, auth=HTTPBasicAuth('', pat))
    logging.info(f'get_git_repo_list_from_prj:{response.status_code}')

    repo_list = []
    if(response.status_code == 200):
        res_obj = json.loads(response.text)
        for repo in res_obj['value']:
            logging.info(f'get_git_repo_list_from_prj:{repo}')
            repo_list.append({
                'url':repo['remoteUrl'],
                'name':repo['name']})
    else:
        raise RuntimeError(f'get_git_repo_list_from_prj failed:{response.status_code}')  
    return repo_list      

def download_repo(repo_url,path):
    
    cmd = 'git -c ' +  f'http.extraHeader="Authorization: Basic {B64_PAT}"'
    cmd += f' clone {repo_url} "{path}"'
    ret = os.system(cmd)
    return ret >> 8 

def read_only_handler(func, path, exc_info):
    if not os.access(path,os.W_OK):
        os.chmod(path,stat.S_IWRITE)
        func(path)
    else:
        raise



def clean_folder(dir_path):
    try:
        if(os.path.exists(dir_path)):  
            logging.info(f'clean_folder:{dir_path}')
            shutil.rmtree(dir_path,onerror=read_only_handler)
        
        logging.info(f'clean_folder:{dir_path} not found')
    
    except OSError as e:
        logging.error(f'clean_folder error:{e}')   

def get_all_repo_urls():
    all_repo_list = []
    
    prj_list = get_prj_list(org_name,pat)
    logging.info(prj_list)    

    if(prj_list is None):
        logging.info('no prjs.')
        return
    
    prj_list = prj_list['value']
    
    for prj in prj_list:
        repos = get_git_repo_list_from_prj(org_name,prj['name'],pat)
        all_repo_list.extend(repos)
    return all_repo_list

def create_folder(dir_folder):
    if(os.path.exists(dir_folder)):
        logging.info(f'create_folder:{dir_folder} already exist')
        return

    os.mkdir(dir_folder)
    logging.info(f'create_folder:{dir_folder} done')
    
def init_backup_folder(backup_folder):
    
    clean_folder(backup_folder)
    create_folder(backup_folder)

def main():
    
    init_logging()
    init_backup_folder(backup_folder)

    try:
        repos = get_all_repo_urls()
        logging.info(f'all repos:{repos}')
        
        for repo in repos:
            saving_folder = os.path.join('.',backup_folder,f"{repo['name']}_{today_str}")
            r = download_repo(repo['url'],saving_folder)
            if(r!=0):
                # break here to error handler
                raise RuntimeError(f'download_repo error:{repo["url"]},{saving_folder}')
            logging.info(f'download_repo done:{repo["url"]},{saving_folder},{r}')
            
      
    except Exception as e:
        logging.error(e)
        # other handling method like sending emails etc    
    


if __name__ == '__main__':
    main()