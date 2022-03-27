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

Broadcast algorithm (partially implemented):
- Gossip
- When a peer gets a broadcast message, she checks if the message was received earlier
   (via Bloom filter, which updates every 10 min)

Persistence (not implemented yet):
- Store chat history in ipfs
- To recover chat history a user should remember chat data hash and at least one peer should hold the chat file in ipfs
- Chat history is encrypted with the chat secret key

Total order is not guaranteed.

How to run:
```bash
python3 main.py --config config_examples/alice.json
```