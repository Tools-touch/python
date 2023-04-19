from Cryptodome import Random
from Cryptodome.PublicKey import RSA
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 as PKCS1_cipher  
import base58
import hashlib
import binascii
import mnemonic
from mnemonic import Mnemonic
from Cryptodome.PublicKey import RSA
import dataset
import json
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA
from Cryptodome.Signature import PKCS1_v1_5 as PKCS1_signature

class rsa_controller:
    def get_pri_pub_keys_by_mnemonic_words(): #通过助记词的方式生成公私钥
        # 生成助记词
        from mnemonic import Mnemonic
        mnemo = Mnemonic("english") # chinese_simplified
        #通过指定不同的助记词熵，可以生成不同的助记词数量
        mnemonic_words = mnemo.generate(strength=128) # [128, 160, 192, 224, 256]
        print("助记词: ", mnemonic_words)

        # 生成 RSA 公私钥
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        # 将私钥写入文件
        with open("private_key.pem", "wb") as f:
            f.write(private_key)
        # 将公钥写入文件
        with open("public_key.pem", "wb") as f:
            f.write(public_key)
        return {'public_key':public_key,'private_key':private_key,'mnemonic_words':mnemonic_words}

    def restored_pri_pub_keys_by_mnemonic_words(mnemonic_words): #此函数用于通过助记词来还原出RSA密钥对
        # 通过助记词还原出公私钥
        seed = mnemo.to_seed(mnemonic_words)
        key = RSA.import_key(private_key, passphrase=seed)
        # print("还原后的公钥: ", binascii.hexlify(key.publickey().export_key(format='DER')).decode('utf-8'))
        # print("还原后的私钥: ", binascii.hexlify(key.export_key(format='DER', pkcs=8)).decode('utf-8'))

        with open("restored_private_key.pem", "wb") as f:
            f.write(key.export_key())

        with open("restored_public_key.pem", "wb") as f:
            f.write(key.publickey().export_key())

        return {'public_key':key.publickey().export_key(),'private_key':key.export_key()}

    
    

    def get_key(key_file):
        with open(key_file) as f:
            data = f.read()  # 获取，密钥信息
            key = RSA.importKey(data)
        return key


    def encrypt_data(public_key,msg): #加密
        cipher = PKCS1_cipher.new(public_key)  # 生成一个加密的类
        encrypt_text = base64.b64encode(cipher.encrypt(msg.encode()))  # 对数据进行加密
        return encrypt_text.decode()  # 对文本进行解码码


    def decrypt_data(private_key,encrypt_msg): #解密
        cipher = PKCS1_cipher.new(private_key)  # 生成一个解密的类
        back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)  # 进行解密
        return back_text.decode()  # 对文本内容进行解码


    def rsa_private_sign(private_key,data): #签名
        signer = PKCS1_signature.new(private_key)  # 设置签名的类
        digest = SHA.new()  # 创建sha加密的类
        digest.update(data.encode())  # 将要加密的数据进行sha加密
        sign = signer.sign(digest)  # 对数据进行签名
        # 对签名进行处理
        signature = base64.b64encode(sign)  # 对数据进行base64加密
        signature = signature.decode()  # 再进行编码
        return signature  # 返回签名


    def rsa_public_check_sign(public_key,text, sign): #验签
        verifier = PKCS1_signature.new(public_key)  # 生成验证信息的类
        digest = SHA.new()  # 创建一个sha加密的类
        digest.update(text.encode())  # 将获取到的数据进行sha加密
        return verifier.verify(digest, base64.b64decode(sign))  # 对数据进行验证，返回bool值
    
    
    
if __name__ == '__main__': 
    rsa_controller.get_pri_pub_keys_by_mnemonic_words()
    msg = "{'name':'YWJ','message':'I love you'}"
    public_key = rsa_controller.get_key('./public_key.pem')  # 读取公钥信息
    private_key = rsa_controller.get_key('./private_key.pem')  # 读取私钥信息
    

    
    
    # 加密开始
    encrypt_text = rsa_controller.encrypt_data(public_key,msg)  # 加密消息内容
    sign = rsa_controller.rsa_private_sign(private_key,msg) #签名（通过对消息进行签名）
    print('encrypt_text:',encrypt_text,'\n')
    print('sign:',sign,'\n')
    # 加密结束
    
    
    #解密开始
    if rsa_controller.rsa_public_check_sign(public_key,msg, sign) == True:
        decrypt_text = rsa_controller.decrypt_data(private_key,encrypt_text)  # 解密
        print('decrypt_text:',decrypt_text,'\n')
    
        
    else:
        print('验签失败')
        
    #解密结束
