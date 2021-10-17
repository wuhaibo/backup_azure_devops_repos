# Backup Azure Devops Repos  

## Introduction 

Azure devops formerly known as visual studio team service  is a SAAS for devops. It is a good practice to back up the source code regularly or even, it may be required by the company. However, there is no out of box solution [according to microsoft](https://developercommunity.visualstudio.com/t/backup-azure-devops-data/609097).  

 
Although Microsoft does commit to keep data safe:

* [azure devops data is saved at azure storage and azure sql, both are backed up in 2 regions in the same geography.](https://docs.microsoft.com/en-us/azure/devops/organizations/security/data-protection?view=azure-devops)
* [azure devops offers a 99.9% uptime SLA guarantee.](https://azure.microsoft.com/en-us/support/legal/sla/azure-devops/v2_0/)


But we have no control over the backup mentioned above. Here I recommend several ways to do the backup:

1. use [Backrightup](https://cloud.netapp.com/blog/5-considerations-before-you-backup-on-azure) and [integrate using its plugin into azure devops](https://marketplace.visualstudio.com/items?itemName=Backrightup.build-release-task). Very easy and it can backup not only source code but also pipelines. Good service good price. The cost is per repo, therefore if you have many repositories, [the price might be high.](https://backrightup.com/) 
2. use cron job on vm use `git clone` to copy the repo. The drawback is that every time when there is a new repo, you have to change the cron job. 
3. use [azure devops rest api](https://docs.microsoft.com/en-us/rest/api/azure/devops/git/repositories/list?view=azure-devops-rest-6.0) to programmably backup the source code.

Option 1 and 2 are pretty obvious. 
Let us check how we could backup the repo based on the third option.

## Backup Azure Devops Repos

This solution is based on python, so that it could be used in either windows or linux environment. 

### 1. Get an Azure DevOps API personal access token(PAT)
- go to right upper corner click personal access tokens.

<img src="https://res.cloudinary.com/dr8wkuoot/image/upload/v1634310224/blog/pat1_sjjugr.jpg"/>

- specify required fields in following picture to create a pat and copy it. (make sure the pat has code reading right)

<img src="https://res.cloudinary.com/dr8wkuoot/image/upload/v1634310692/blog/pat2_y2zr7e.jpg"/>


### 2. Clone the backup code based on python

The source code could be found at [here at github](https://github.com/wuhaibo/backup_azure_devops_repos.git). Clone it and replace the organization and PAT with your own data. 

The code uses azure devops rest api to get project list and then all repos url based on project list. At last, the code calls git cmd to clone the repo. 

### 3. Run Backup Code as Cron or Scheduler Jobs
Depending on ur environment, you could run the backup code in windows as a scheduler job or in linux as cron job. Or you could even run it as function app in azure. 




