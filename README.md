# Decentralized chat with trash traffic

Scenario: 
1. User, who knows at least one peer address, starts a server and sends the peer his address
2. The peer broadcasts new user address to all known peers
3. Every chat has its secret key, which should be known by participants (by some reliable channel, not the chat)
4. When a user sends a message to a chat, she encrypts it via the secret key and broadcasts the encrypted message
5. Everyone who knows the secret key (therefore belongs to the chat room) can decrypt the message
6. A user can belong to several chats (know several secret keys)

Broadcast algorithm:
- When a peer gets a broadcast message, it checks if he got it earlier
   (via Bloom filter, which updates every 10 min)


