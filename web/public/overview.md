# CopilotJ

## Development

This project contains three parts:

1. **Agent**: The core logic that understands user requests, interacts with AI models, and orchestrates tasks. It
   communicates with the ImageJ plugin via the Bridge server to control ImageJ.
2. **ImageJ plugin**: A Java-based plugin running within ImageJ. It listens for commands from the Agent (relayed by the
   Bridge server), executes these commands using ImageJ's APIs, and sends results or state changes back.
3. **Bridge server**: A communication hub that facilitates interaction between the Python-based Agent and the
   Java-based ImageJ plugin. It typically uses WebSockets to relay messages and commands.
