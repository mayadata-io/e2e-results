# GCP platform specific code and scripts
## Google Cloud provisioning and setting up Kubernetes cluster using KOPS
These playbook act as a wrapper class for all the `kops`, `gsutil` & `gcloud` command. 

### Prerequisites
- kubectl
- gcloud
- kops

### Setting up

- Run `gcloud init`, and authenticate into your google account linked with the Google Cloud

### Running

- Run `create-vpc.yml` using anisble-playbook, that will create a Virtual Private Cloud
```bash
ansible-playbook create-vpc.yml -vv
```
- Run `create-k8s-cluster`, this will create a Bucket with Random name and the cluster with same name with `.k8s.local` added.
Pass the Project name and Node count
```bash
ansible-playbook create-k8s-cluster.yml -vv --extra-vars "PROJECT=<project-name> NODES=1"
```
Cluster is Created!

### Deleting the cluster

- Run `delete-k8s-cluster`, this will delete the cluster as well as the Bucket associated
Pass the cluster name in `NAME`
```bash
ansible-playbook delete-k8s-cluster.yml -vv --extra-vars "NAME=openebs-e2e-zo211u"
```
- Run `delete-vpc` to delete the existing VPC (if required)
```bash
ansible-playbook delete-vpc.yml -vv
```

