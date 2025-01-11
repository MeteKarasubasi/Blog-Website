# 🌟 Modern Django Blog Projesi

Modern, özelleştirilebilir ve kullanıcı dostu bir blog platformu. Django 5.1 ile geliştirilmiş, Bootstrap 5 ile tasarlanmış tam özellikli bir blog uygulaması.

## ✨ Özellikler

### 📝 Blog Yazıları
- Zengin metin editörü (CKEditor) ile yazı oluşturma ve düzenleme
- Öne çıkan görsel desteği
- Otomatik görsel boyutlandırma ve optimizasyon
- Yazı durumları (taslak/yayında)
- SEO dostu URL yapısı
- Okunma sayısı takibi
- Yazı özeti ve etiketleme sistemi

### 👥 Kullanıcı Yönetimi
- Özel kullanıcı modeli
- Email ile kayıt ve doğrulama
- Sosyal medya ile giriş (AllAuth entegrasyonu)
- Profil sayfası ve avatar
- Şifre sıfırlama ve değiştirme
- Kullanıcı rolleri (admin/yazar/okuyucu)

### 💬 Etkileşim
- Yorum sistemi
- İletişim formu
- Kategori ve etiket filtreleme
- Arama fonksiyonu
- Arşiv görünümü
- SSS (Sıkça Sorulan Sorular) bölümü

### 🎨 Tasarım ve UI
- Responsive tasarım (Bootstrap 5)
- Modern ve temiz arayüz
- Özelleştirilebilir temalar
- Kullanıcı dostu yönetim paneli
- Animasyonlu geçişler
- Görsel önbelleğe alma

### 🔧 Teknik Özellikler
- PostgreSQL veritabanı desteği
- Resim yükleme ve işleme (Pillow)
- Form yönetimi (Crispy Forms)
- Sayfalama sistemi
- Hit counter entegrasyonu
- SMTP email desteği

## 🚀 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/blog-projesi.git
cd blog-projesi
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv env
# Windows için
env\Scripts\activate
# Linux/Mac için
source env/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanını oluşturun:
```bash
python manage.py migrate
```

5. Süper kullanıcı oluşturun:
```bash
python manage.py createsuperuser
```

6. Projeyi çalıştırın:
```bash
python manage.py runserver
```

## ⚙️ Gereksinimler

- Python 3.8+
- Django 5.1.2
- PostgreSQL
- Diğer gereksinimler requirements.txt dosyasında listelenmiştir

## 📦 Kullanılan Paketler

- Django==5.1.2
- psycopg2-binary==2.9.10
- Pillow==11.0.0
- python-dotenv==1.0.1
- django-crispy-forms==2.3
- crispy-bootstrap5==2024.10
- django-ckeditor
- django-allauth
- django-hitcount

## 🔐 Güvenlik

- Debug modu production ortamında kapalı olmalıdır
- SECRET_KEY güvenli bir şekilde saklanmalıdır
- Email şifreleri ve hassas bilgiler environment variables olarak tanımlanmalıdır
- HTTPS kullanımı önerilir

## 📱 Ekran Görüntüleri

[Ekran görüntüleri buraya eklenecek]

## 🌐 Demo

[Demo site linki buraya eklenecek]

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

İsim - [@twitter_handle](https://twitter.com/twitter_handle)
Email - email@example.com
Proje Linki: [https://github.com/kullaniciadi/blog-projesi](https://github.com/kullaniciadi/blog-projesi)

## 🙏 Teşekkürler

- Django Topluluğu
- Bootstrap Ekibi
- Tüm katkıda bulunanlara 