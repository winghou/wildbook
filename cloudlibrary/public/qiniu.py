# codding: utf-8
# flake8: noqa

from qiniu import Auth, put_file, BucketManager

QINIU_ACCESS_KEY = "s6ptDyF0y2BwtEMryo-Mm3A045HBPbKY4jNQRksw"
QINIU_SECRET_KEY = "o1Ue_r7PRNMJ5CEnw0GP8gaRA6Bn6AkJkcN2WGDE"


def save_file_to_qiniu(img_path, img_name):
    access_key = QINIU_ACCESS_KEY
    secret_key = QINIU_SECRET_KEY
    q = Auth(access_key, secret_key)
    bucket_name = 'wildbook'
    key = img_name
    token = q.upload_token(bucket_name, key, 3600)
    local_file = img_path
    put_file(token, key, local_file)
    pass


def del_pic_from_qiniu(img_name):
    img_name = str(img_name).split("/")[-1]
    access_key = QINIU_ACCESS_KEY
    secret_key = QINIU_SECRET_KEY
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = "wildbook"
    key = img_name
    bucket.delete(bucket_name, key)
    # print("要删除的图片:", img_name)
    # ret, info = bucket.delete(bucket_name, key)
    # 得到返回的状态码
    # print(info)
    # try:
    #     print("1", info.status_code)
    # except:
    #     pass
    pass

