# IOUeth

An IOU Smart Contract for Ethereum (Vyper)

See stateless version at https://github.com/iRyanBell/ioueth_lite

**Contract Address:**
0xba556f09a49764a757c42f384116de7125900d70

### ABI:

```json
[
  {
    "name": "Iou",
    "inputs": [
      { "type": "address", "name": "_from", "indexed": false },
      { "type": "address", "name": "_to", "indexed": false }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "iou",
    "outputs": [],
    "inputs": [{ "type": "address", "name": "_to" }],
    "constant": false,
    "payable": false,
    "type": "function",
    "gas": 38619
  },
  {
    "name": "iou_balance",
    "outputs": [{ "type": "int128", "name": "out" }],
    "inputs": [
      { "type": "address", "name": "_a" },
      { "type": "address", "name": "_b" }
    ],
    "constant": false,
    "payable": false,
    "type": "function",
    "gas": 2778
  }
]
```

**View on Etherscan:**
https://etherscan.io/address/0xba556f09a49764a757c42f384116de7125900d70

### Functions

- iou(recipient): Sends an IOU to an Ethereum address.
- iou_balance(sender, recipient): Returns +/- IOU balance between sender -> recipient.
