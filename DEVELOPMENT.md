# CopilotJ Development

This project contains three parts:

1. **Agent**: The core logic that understands user requests, interacts with AI models, and orchestrates tasks. It
   communicates with the ImageJ plugin via the Bridge server to control ImageJ.
2. **ImageJ plugin**: A Java-based plugin running within ImageJ. It listens for commands from the Agent (relayed by the
   Bridge server), executes these commands using ImageJ's APIs, and sends results or state changes back.
3. **Bridge server**: A communication hub that facilitates interaction between the Python-based Agent and the
   Java-based ImageJ plugin. It typically uses WebSockets to relay messages and commands.

Run the bridge server:

```bash
python -m copilotj.server
```

The server is designed to be stable due to its minimal and focused design.

Run the plugin (with FIJI):

```bash
cd plugin && \
  mvn exec:java -D"exec.mainClass=copilotj.DefaultCopilotJBridgeService" -D"ij.debug=true"
```

Run the multiagent:

```bash
python -m copilotj.multiagent
```

If you make changes to the Java code, restart the plugin to apply the updates.

Once everything is running, look for the message `Bridge WebSocket connection established` in the server console to
confirm that the connection is active.

### Manual Plugin Deployment

If you prefer to manually deploy the plugin to your ImageJ/FIJI installation:

1. **Build the plugin JAR:**
   Navigate to the `plugin` directory and build the package. This will create the plugin JAR file (e.g.,
   `CopilotJBridge-1.0.0.jar`) in the `plugin/target/` directory.
   ```bash
   cd plugin && mvn package
   ```
2. **Copy Dependency Jars:**
   The plugin requires several dependency JARs. You need to copy these into your ImageJ/FIJI `plugins` or `jars`
   directory along with the plugin JAR itself. A common way to gather these is using the `maven-dependency-plugin`.
   You can add this to your `pom.xml` or run a command like:
   ```bash
   cd plugin && mvn dependency:copy-dependencies
   ```
   This will typically copy the dependencies to `plugin/target/dependency/`.
3. **Manually Copy Jars to ImageJ/FIJI:**
   Copy the main plugin JAR (e.g., `plugin/target/copilotj_plugin-1.0.0.jar`) and all the JAR files from
   `plugin/target/dependency/` into your ImageJ or FIJI's `plugins/` directory (or `jars/` directory, depending on your
   ImageJ setup).
   **Important:** Ensure you do not introduce conflicting versions of JARs already present in your ImageJ/FIJI
   installation. If ImageJ/FIJI already provides a specific library, it's often better to use the existing one, unless
   the plugin requires a newer version and you've confirmed compatibility. Remove any older or different versions of
   the same libraries to avoid class loading issues.
4. **Restart ImageJ/FIJI:**
   After copying the JAR files, restart ImageJ/FIJI for the changes to take effect.
