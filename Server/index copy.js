const crypto = require('crypto');

// The encrypted message and initialization vector (IV)
const encryptedMessage = 'f12f6f8c5e6d8a1c815a554a2bf84f706c5157c1bc5edf1bab28f0848d9a0a740b16f0fcea9ace0ad2fe35e4b468a806fcc812d993c297645d316a25fc90a85d6c8e73812f355ccd75bda6f1fce45677';
const iv = Buffer.alloc(16, 0);
// The secret key used for encryption
const secretKey = 'Ae7nM4dG53Lo7pA4pqr474tgf47GT5z=';

// Convert the encrypted message and IV from hex to buffers
const encryptedBuffer = Buffer.from(encryptedMessage, 'hex');
const decipher = crypto.createDecipheriv('aes-256-cbc', secretKey, iv);
let decrypted = decipher.update(encryptedBuffer);
decrypted = Buffer.concat([decrypted, decipher.final()]);
const decryptedMessage = decrypted.toString('utf8');

console.log(decryptedMessage);
