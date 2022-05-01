import os
from PIL import Image
from flask import url_for, current_app

def add_profile_picture(picture_upload, username) : 
    filename = picture_upload.filename
    # 파일 확장자 확인용 : "mypicture.jpg" -> "jpg" 
    extension_type = filename.split('.')[-1] 
    # 저장할때는 업로드된 파일명 무시하고, 사용자명으로 저장
    save_filename = str(username) + '.' + extension_type
    # 현재 애플리케이션의 root 경로를 가져온후 'static\images\profile'로 이동하여
    # storage_filename 이름으로 파일 저장
    filepath = os.path.join(current_app.root_path, 'static/images/profile', save_filename)
    
    # 모든 이미지를 동일한 크기로 설정
    profile_picture_size = (200, 200) 
    
    # 사용자가 제공
    picture = Image.open(picture_upload)
    
    # 원하는크기(profile_picture_size)대로, 이미지 압축
    picture.thumbnail(profile_picture_size)
    
    picture.save(filepath)
    
    return save_filename