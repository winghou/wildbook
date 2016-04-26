# codding: utf-8
# flake8: noqa

from qiniu import Auth, put_file


def save_file_to_qiniu(img_path, img_name):
    access_key = "s6ptDyF0y2BwtEMryo-Mm3A045HBPbKY4jNQRksw"
    secret_key = "o1Ue_r7PRNMJ5CEnw0GP8gaRA6Bn6AkJkcN2WGDE"
    q = Auth(access_key, secret_key)
    bucket_name = 'wildbook'
    key = img_name
    token = q.upload_token(bucket_name, key, 3600)
    local_file = img_path
    ret, info = put_file(token, key, local_file)
    print(info)
    pass
