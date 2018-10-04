# AWS platform-specific code and scripts
## Amazon web service and setting up Kubernetes cluster using KOPS
This playbook acts as a wrapper class for all the `kops`, `aws`  command. 

### Prerequisites
- kubectl
- aws
- kops

### Setting up

- Run `aws configure`, and authenticate into your aws account linked with the AWS Cloud

### Running

- Run `pre-requisite` using anisble-playbook, that will create a Virtual Private Cloud, Subnet and Internet-Gateway
```bash
ansible-playbook pre-requisite.yml -vv
```
- Run `create-aws-cluster.yml`, this will create a Bucket and the cluster, cluster name ended with `.k8s.local`.
Pass the arguments
```bash
ansible-playbook create-aws-cluster.yml -vv --extra-vars "build=100"
```

### Deleting the cluster

- Run `delete-aws-cluster`, this will delete the cluster as well as the Bucket associated with it.
Pass the cluster name in command line argument
```bash
ansible-playbook delete-aws-cluster.yml -vv --extra-vars "build=100"
```
- Run `delete-pre-requisite` to delete the existing VPC, Subnets and Internet Gateway (if required)
```bash
ansible-playbook delete-pre-requisite.yml -vv
```

