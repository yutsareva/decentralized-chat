# Decentralized chat with trash traffic

Idea: every peer gets all messages from her connectivity component.
Belonging to a chat room is equivalent to knowing the chat room secret key the messages are encrypted with.

Scenario: 
1. User, who knows at least one peer address, starts a server and sends the peer his address
2. The peer broadcasts new user address to all known peers
3. Every chat has its secret key, which should be known by participants (by some reliable channel, not the chat)
4. When a user sends a message to a chat, she encrypts it via the secret key and broadcasts the encrypted message
5. Everyone who knows the secret key (therefore belongs to the chat room) can decrypt the message
6. A user can belong to several chats (know several secret keys)

Broadcast algorithm:
- Gossip
- When a peer gets a broadcast message, she checks if the message was received earlier (via Bloom filter)

Persistence:
- Store chat history locally
- To recover chat history it should be stored at least one peer
- Chat history is encrypted with the chat secret key

Total order is not guaranteed.

Menu options (press Ctrl+C):
- print 'chat CHAT_NAME' to change chat name
- print 'exit' to exit
- print 'load history' to send request for receiving chat history
- print 'show history' to output chat history

How to run:
```bash
python3 main.py --config config_examples/alice.json
```