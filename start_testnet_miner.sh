pm2 start python --name miner -- neurons/miner.py --neuron.model_path ./mining_models/miner.pth --netuid 168 --subtensor.network test --wallet.name default --wallet.hotkey testnet_miner --axon.port 8091 --blacklist.force_validator_permit True
