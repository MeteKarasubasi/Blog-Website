# Modern Django Blog Projesi 🚀

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/MeteKarasubasi/Blog-Website)
![GitHub issues](https://img.shields.io/github/issues/MeteKarasubasi/Blog-Website)
![GitHub stars](https://img.shields.io/github/stars/MeteKarasubasi/Blog-Website)
![GitHub forks](https://img.shields.io/github/forks/MeteKarasubasi/Blog-Website)
![GitHub license](https://img.shields.io/github/license/MeteKarasubasi/Blog-Website)

</div>

Modern ve teknoloji odaklı bir blog platformu. Django 5.1 ve Bootstrap 5 ile geliştirilmiş, dark mode tasarıma sahip, kullanıcı dostu bir blog sistemi.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Teknolojiler](#-teknolojiler)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Güvenlik](#-güvenlik-tavsiyeleri)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-iletişim)

## ✨ Özellikler

### 📝 Blog Yönetimi
- Modern ve şık dark mode arayüz
- Zengin metin editörü (CKEditor) ile yazı oluşturma
- Kategori ve etiket sistemi
- Görüntülenme sayısı takibi
- Yorum sistemi

### 👤 Kullanıcı Yönetimi
- Özelleştirilebilir kullanıcı profilleri
- Sosyal medya entegrasyonu
- Güvenli şifre değiştirme ve sıfırlama sistemi
- E-posta doğrulama

### 🛠️ Admin Paneli
- Kapsamlı yönetim arayüzü
- İstatistik takibi
- İçerik moderasyonu
- Kullanıcı yönetimi

### 🎨 Modern Tasarım
- Responsive tasarım
- Dark mode
- Neon efektler
- Modern animasyonlar
- Kullanıcı dostu arayüz

## 🖼️ Ekran Görüntüleri

### Ana Sayfa
![Blog Ana Sayfa](screenshots/blog-home.png)
*Modern dark mode tasarımlı ana sayfa*

### Yönetim Paneli
![Yönetim Paneli](screenshots/admin-dashboard.png)
*İstatistikler ve içerik yönetimi*

### Yazı Ekleme
![Yazı Ekleme](screenshots/post-add.png)
*Zengin metin editörü ile yazı ekleme*

### Profil Sayfası
![Profil](screenshots/profile.png)
*Özelleştirilebilir kullanıcı profili ve sosyal medya bağlantıları*

### Hakkımda Sayfası
![Hakkımda](screenshots/about.png)
*Kişisel bilgiler ve tanıtım*

### İletişim Formu
![İletişim](screenshots/contact.png)
*Modern tasarımlı iletişim formu*

## 🛠️ Teknolojiler

### Backend
- [Django 5.1](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Django Allauth](https://django-allauth.readthedocs.io/)
- [Django CKEditor](https://django-ckeditor.readthedocs.io/)

### Frontend
- [Bootstrap 5](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- JavaScript
- HTML5/CSS3

### Diğer
- SMTP (Gmail) E-posta Servisi
- Django Hitcount
- Django Crispy Forms

## 📦 Gereksinimler

Projeyi çalıştırmak için aşağıdaki gereksinimlere ihtiyacınız var:

- Python 3.8+
- PostgreSQL
- pip (Python Paket Yöneticisi)
- Virtual Environment

## ⚙️ Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/MeteKarasubasi/Blog-Website.git
cd Blog-Website
```

2. Virtual environment oluşturun:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyası oluşturun ve gerekli değişkenleri ayarlayın:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

5. Veritabanını oluşturun:
```bash
python manage.py migrate
```

6. Admin kullanıcısı oluşturun:
```bash
python manage.py createsuperuser
```

7. Statik dosyaları toplayın:
```bash
python manage.py collectstatic
```

8. Uygulamayı çalıştırın:
```bash
python manage.py runserver
```

## 💻 Kullanım

1. Admin paneline erişmek için:
   - `http://127.0.0.1:8000/admin/` adresine gidin
   - Oluşturduğunuz superuser bilgileriyle giriş yapın

2. Blog yazısı eklemek için:
   - Admin panelinden "Posts" bölümüne gidin
   - "Add Post" butonuna tıklayın
   - Gerekli alanları doldurun ve kaydedin

3. Kullanıcı işlemleri:
   - Kayıt olmak için: `/accounts/signup/`
   - Giriş yapmak için: `/accounts/login/`
   - Profil düzenlemek için: `/profile/edit/`

## 🔒 Güvenlik Tavsiyeleri

- DEBUG modunu production ortamında kapatın
- SECRET_KEY'i güvenli bir şekilde saklayın
- ALLOWED_HOSTS'u production ortamında düzenleyin
- Güvenli bir PostgreSQL yapılandırması kullanın
- E-posta ayarlarını güvenli bir şekilde yapılandırın
- `.env` dosyasını `.gitignore` listesine ekleyin
- Düzenli olarak güvenlik güncellemelerini kontrol edin

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/amazing`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📧 İletişim

İsmail Mete Karasubasi
- LinkedIn: [İsmail Mete Karasubasi](https://www.linkedin.com/in/ismail-mete-karasuba%C5%9F%C4%B1-253077225/)
- Email: ismailmetekarasubasi@gmail.com
- GitHub: [@MeteKarasubasi](https://github.com/MeteKarasubasi)

## 🌟 Proje Durumu

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/MeteKarasubasi/Blog-Website)
![GitHub code size](https://img.shields.io/github/languages/code-size/MeteKarasubasi/Blog-Website)
![GitHub top language](https://img.shields.io/github/languages/top/MeteKarasubasi/Blog-Website)

Proje Linki: [https://github.com/MeteKarasubasi/Blog-Website](https://github.com/MeteKarasubasi/Blog-Website)

---
⭐️ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 
