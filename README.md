This documentation provides a step-by-step guide on setting up Docker on an Ubuntu system, deploying Keycloak as a Docker container, and integrating Keycloak with Cloudflare Access. Keycloak is an open-source identity and access management solution that enables secure authentication and authorization for applications and services. Cloudflare Access, part of Cloudflare’s Zero Trust platform, secures your internal applications without the need for a VPN, providing seamless, identity-based access control. By following this guide, you will learn how to install and configure Docker, deploy Keycloak as a container, and integrate Keycloak as an identity provider (IdP) with Cloudflare Access to enhance the security and accessibility of your applications. This integration will ensure that only authenticated users can access your protected resources, leveraging the power of both Keycloak’s comprehensive identity management capabilities and Cloudflare’s advanced security features.

### **Steps to Deploy**

1. **Remove Previous Containers and Volumes**
    
    Ensure any previous containers and volumes are removed:
    
    ```bash
    sudo docker-compose down -v
    
    ```
    
2. **Clean Up Any Existing PostgreSQL Data Directory**
    
    Ensure the old PostgreSQL data directory is removed:
    
    ```bash
    sudo rm -rf /home/arun/docker/keycloak/postgresql_data
    
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

https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/generic-oidc/

1> Find openid-config

```arduino
http://10.0.0.162:8080/realms/master/.well-known/openid-configuration
```

Answer:


```arduino
Client ID
Client secret
Auth URL: https://keycloak.arunblog.org/realms/master/protocol/openid-connect/auth
Token URL: https://keycloak.arunblog.org/realms/master/protocol/openid-connect/token
Certificate URL: The jwks_uri endpoint of your IdP to allow the IdP keys to sign the tokens
 "jwks_uri": "https://keycloak.arunblog.org/realms/master/protocol/openid-connect/certs
```

```arduino
"authorization_endpoint": "https://keycloak.arunblog.org/realms/myrealm/protocol/openid-connect/auth",
"token_endpoint": "https://keycloak.arunblog.org/realms/myrealm/protocol/openid-connect/token",
"jwks_uri": "https://keycloak.arunblog.org/realms/myrealm/protocol/openid-connect/certs"
```
