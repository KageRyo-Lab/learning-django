import datetime
from typing import List, Optional
from django.contrib.auth import authenticate
from ninja import NinjaAPI, Schema
from ninja.security import django_auth, HttpBearer, HttpBasicAuth
from .models import Place, Photo, Tag, Device

api = NinjaAPI()

# 設定 API 權限帳號
class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = authenticate(username = username, password = password)

# 定義瀏覽人數的 Schema
class VisitSchema(Schema):
    today: int
    total: int

# 定義標籤的 Schema
class TagSchema(Schema):
    name: str
    
# 定義設備的 Schema
class DeviceSchema(Schema):
    name: str
    
# 定義照片的 Schema
class PhotoSchema(Schema):
    name: str = "照片"
    path: str = '/'

# 定義店家的 Schema
class PlaceSchema(Schema):
    id: int
    name: str
    address: str
    phone_number: str
    photos: Optional[List[PhotoSchema]]
    website: str
    introduction: str
    pub_date: datetime.datetime
    tags: List[TagSchema]
    devices: List[DeviceSchema]

# GET：計算瀏覽人數
@api.get("visits", response=VisitSchema)
def get_visits(request):
    visits = request.session.get('visits', 0)
    request.session['visits'] = visits + 1
    return VisitSchema(
        today = visits,
        total = visits
    )

# GET：取得所有標籤
@api.get("tags", response=List[TagSchema])
def get_tags(request):
    tags = Tag.objects.all()
    return tags

# GET：取得所有設備
@api.get("devices", response=List[DeviceSchema])
def get_devices(request):
    devices = Device.objects.all()
    return devices

# GET：取得所有店家
@api.get("places", response=List[PlaceSchema])
def get_places(request, food_style: Optional[int] = None, payment_type: Optional[int] = None):
    # 初始化篩選字典
    filters = {}
    
    # 根據 food_style 參數篩選
    if food_style is not None:
        filters['tags__id'] = food_style
        
    # 根據 payment_type 參數篩選
    if payment_type is not None:
        filters['devices__id'] = payment_type

    # 根據篩選條件取得店家
    places = Place.objects.filter(**filters).prefetch_related('photo_set', 'tags', 'devices')
    
    # 格式化回傳結果
    result = [
        PlaceSchema(
            id=place.id,
            name=place.name,
            address=place.address,
            phone_number=place.phone_number,
            photos=[PhotoSchema(name=photo.name, path=photo.file.url) for photo in place.photo_set.all()],
            website=place.website,
            introduction=place.introduction,
            pub_date=place.pub_date,
            tags=[TagSchema(name=tag.name) for tag in place.tags.all()],
            devices=[DeviceSchema(name=device.name) for device in place.devices.all()]
        )
        for place in places
    ]
    
    return result

# GET：取得特定店家
@api.get("place", response=PlaceSchema)
def get_place(request, id: int):
    place = Place.objects.prefetch_related('photo_set', 'tags', 'devices').get(id=id)
    result = PlaceSchema(
        id=place.id,
        name=place.name,
        address=place.address,
        phone_number=place.phone_number,
        photos=[PhotoSchema(name=photo.name, path=photo.file.url) for photo in place.photo_set.all()],
        website=place.website,
        introduction=place.introduction,
        pub_date=place.pub_date,
        tags=[TagSchema(name=tag.name) for tag in place.tags.all()],
        devices=[DeviceSchema(name=device.name) for device in place.devices.all()]
    )
    return result
    
# POST：新增標籤資料
@api.post("tags", auth=BasicAuth())
def post_tag(request, pay_load: TagSchema):
    tag = Tag.objects.create(**pay_load.dict())
    return {"id": tag.id}