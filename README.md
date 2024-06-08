This documentation provides a step-by-step guide on setting up Docker on an Ubuntu system, deploying Keycloak as a Docker container, and integrating Keycloak with Cloudflare Access. Keycloak is an open-source identity and access management solution that enables secure authentication and authorization for applications and services. Cloudflare Access, part of Cloudflare’s Zero Trust platform, secures your internal applications without the need for a VPN, providing seamless, identity-based access control. By following this guide, you will learn how to install and configure Docker, deploy Keycloak as a container, and integrate Keycloak as an identity provider (IdP) with Cloudflare Access to enhance the security and accessibility of your applications. This integration will ensure that only authenticated users can access your protected resources, leveraging the power of both Keycloak’s comprehensive identity management capabilities and Cloudflare’s advanced security features.

### **Steps to Install Docker on Ubuntu**

### **Step 1: Update Your System**

Before installing Docker, it's important to update your package list and install necessary dependencies.

```bash
sudo apt-get update
sudo apt-get upgrade

```

### **Step 2: Install Required Packages**

Install packages that allow apt to use a repository over HTTPS.

```bash
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

```

### **Step 3: Add Docker’s Official GPG Key**

Add Docker's official GPG key to your system.

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

```

### **Step 4: Add Docker Repository**

Add the Docker repository to your APT sources.

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

```

### **Step 5: Update Package Database**

Update the package database with the Docker packages from the newly added repo.

```bash
sudo apt-get update

```

### **Step 6: Install Docker**

Now, install Docker.

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io

```

### **Step 7: Verify Docker Installation**

Check the Docker version to verify the installation.

```bash
docker --version

```

You should see output similar to:

```
Docker version 20.10.7, build f0df350

```


### **Steps to Deploy Keycloak**

1. **Remove Previous Containers and Volumes**
    
    Ensure any previous containers and volumes are removed:
    
    ```bash
    sudo docker-compose down -v
    
    ```
    
3. **Deploy the Updated Stack**
    
    Start the containers with the updated configuration:
    
    ```bash
    sudo docker-compose up -d
    
    ```
    
4. **Check the Logs**
    
    Monitor the logs for PostgreSQL and Keycloak to ensure they start correctly:

    ```bash
    sudo docker-compose logs -f postgres
    sudo docker-compose logs -f keycloak

    ```

### **Step-by-Step Guide to Create a Client and Obtain Client Credentials in Keycloak**

1. **Login to Keycloak Admin Console:**
    - Open your web browser and navigate to your Keycloak Admin Console URL (e.g., **`http://<your-keycloak-server>/auth/admin/`**).
    - Login with your admin credentials.
2. **Select the Realm:**
    - From the top left corner, select the realm in which you want to create the client. If you haven't created a custom realm, you can use the default realm (**`master`**), but it is recommended to create a separate realm for your applications.
3. **Navigate to Clients:**
    - In the left-hand sidebar, click on **`Clients`**.
4. **Create a New Client:**
    - Click on the **`Create`** button.
    - Fill in the **`Client ID`** field with a unique identifier for your client (e.g., **`my-client`**).
    - Select **`Client Protocol`**. Usually, it is **`openid-connect`**.
    - Click on **`Save`**.
5. **Configure Client Settings:**
    - After saving, you will be taken to the client configuration page.
    - Under the **`Settings`** tab, configure the following fields:
        - **Root URL**: The base URL of your application (e.g., **`http://localhost:8080`**).
        - **Valid Redirect URIs**: **`https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/callback`**
        - **Base URL**: The base URL of your application (e.g., **`http://localhost:8080`**).
        - **Admin URL**: If applicable, the admin URL for the client.
        - **Web Origins**: Define allowed origins for CORS (Cross-Origin Resource Sharing) (e.g., **`http://localhost:8080`**).
        - **Access Type**: Ensure it is set to **`confidential`**.
6. **Enable Client Authentication:**
    - Scroll down to the **`Authentication`** section.
    - Turn on the **`Client authentication`** toggle.
    - Click on **`Save`**.
7. **Obtain Client Credentials:**
    - After enabling client authentication and saving, go to the **`Credentials`** tab.
    - You will see the **`Client Secret`**. You can copy this value to use it in your application.

### **Example: Client Settings Configuration**

1. **Client ID:** **`my-client`**
2. **Client Protocol:** **`openid-connect`**
3. **Root URL:** **`http://localhost:8080`**
4. **Valid Redirect URIs:** **`https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/callback`**
5. **Base URL:** **`http://localhost:8080`**
6. **Web Origins:** **`http://localhost:8080`**
7. **Access Type:** **`confidential`**

### **Example: Credentials Tab**

- **Client Secret:** **`<generated-client-secret>`**

### **Summary**

By following these steps, you will create a new client in Keycloak, configure it with the specified valid redirect URL, enable client authentication, and obtain the client credentials required for your application to authenticate and interact with Keycloak. Ensure that you securely store the client secret and configure your application to use it when communicating with Keycloak.

## Integrating with Cloudflare as an IDP:


1> Find openid-config
From the below link you can obtain Auth URL, Token URL, and Certificate URL. Client ID and Client secret were already otained in the previous step.

```arduino
http://10.0.0.162:8080/realms/master/.well-known/openid-configuration
```

Answer:


```arduino
Client ID
Client secret
Auth URL: http://10.0.0.162:8080/realms/myrealm/protocol/openid-connect/auth
Token URL: http://10.0.0.162:8080/realms/myrealm/protocol/openid-connect/token
Certificate URL: The jwks_uri endpoint of your IdP to allow the IdP keys to sign the tokens
 "jwks_uri": "http://10.0.0.162:8080/realms/myrealm/protocol/openid-connect/certs
```

2> As you can from step 1, the opendid-configurtaion for keycloak provides my local IP. With Cloudflare Tunnel, you can expose your HTTP resources to the Internet via a public hostname.  
https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/routing-to-tunnel/

```arduino
Client ID
Client secret
Auth URL: http://keycloak.example.com/realms/myrealm/protocol/openid-connect/auth
Token URL: http://keycloak.example.com/realms/myrealm/protocol/openid-connect/token
Certificate URL: The jwks_uri endpoint of your IdP to allow the IdP keys to sign the tokens
 "jwks_uri": "http://keycloak.example.com/realms/myrealm/protocol/openid-connect/certs
```

3> Follow the steps below, use the 5 variables (Auth URL, Token URL, Certificate URL, Client ID and Client secret) obtained above to configure generic-OIDC connection on Cloudflare Access using the below documentation:
https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/generic-oidc/

### **Steps to Add Group Information to Token (client scope) in Keycloak**

With everything we have configured so far, cloudflare can authenticate users created on the keycloak IDP. However, it won't fetch the users group information to create any Cloudflare Access related policies. In roder for Cloudflare to fetch users group information, we need to ad groups to the client scope in keycloak:

1. **Create a Client Scope**:
    - Log in to the Keycloak Admin Console.
    - Select the realm where your application resides.
    - Navigate to **`Client Scopes`** from the left-hand menu.
    - Click on **`Create`**.
2. **Configure the Client Scope**:
    - Provide a name for the client scope, e.g., **`group-scope`**.
    - Click **`Save`**.
3. **Add a Protocol Mapper to the Client Scope**:
    - After saving, you will be redirected to the client scope settings.
    - Go to the **`Mappers`** tab.
    - Click on **`Configure new mapper`**.
    - Select `Group Membership`
    - Configure the mapper as follows:
        - **Name**: **`groups`**
        - **Mapper Type**: **`Group Membership`**
        - **Token Claim Name**: **`groups`**
        - **Full group path**: Choose based on whether you want full paths or just group names.
        - **Add to ID token**: On
        - **Add to access token**: On
        - **Add to userinfo**: On
    - Click **`Save`**.
4. **Assign the Client Scope to Your Client**:
    - Go to **`Clients`** from the left-hand menu.
    - Select your client (the one Cloudflare Access uses).
    - Go to the **`Client Scopes`** tab.
    - In the **`Assigned Default Client Scopes`** section, click on **`Add client scope`**.
    - Select **`group-scope`** and click **`Add`**.
5. **Test the Configuration**:
    - Ensure the Flask app or your OAuth flow setup is updated to request the new scope if necessary.
    - Follow the usual steps to obtain the token.
  

### **Also add 'groups' as OIDC claims on Cloudflare Zero Trust dashboard:**
Navigate to ZT Dashboard > Settings > Authentication > Edit the keycloak OIDC connection:

<img width="661" alt="image" src="https://github.com/arunvl88/keycloak-Zero-Trust/assets/7003647/ee816aa9-37e9-4d33-9aea-8b66df8e147e">


