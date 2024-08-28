import sqlite3
from time import sleep
import datetime
from functools import reduce
import locale
con=sqlite3.connect("Kütüphane.db")
cursor=con.cursor()
locale.setlocale(locale.LC_ALL,"")


class Kütüphane():
    def __init__(self):
        pass
    def __len__(self):
        cursor.execute("Select Adet From kitaplık")
        liste=cursor.fetchall()
        toplam_kitap_sayisi=reduce(lambda x,y:x+y,liste)
        return f"Kitaplığınızda toplam {toplam_kitap_sayisi[0]} kitap bulunmaktadır."  #Kitaplıkta kayıtlı toplam kitap sayısını döner.
    def tablo_olustur(self):
        cursor.execute("Create Table if not exists kitaplık(İsim TEXT,Yazar TEXT,Tür TEXT,Yayınevi TEXT,Sayfa_Sayısı INT,Adet INT)")
        con.commit()   #kütüphane databese sinde kitaplık  isimli bir tablo oluşturur.(Eğer yoksa)
    def tablo_olustur2(self):
        cursor.execute("Create Table if not exists Ödünç_Verilenler(Kitap_İsmi TEXT,Yayınevi TEXT, Kitabın_Yazarı TEXT,Ödünç_Alanın_İsmi TEXT,Ödünç_Alanın_Adresi TEXT,Telefon_Numarası TEXT,Ödünç_Verilme Tarihi DATETIME,Son_Ödünç_Tarihi DATETIME)")
        con.commit()
    def kitap_ekle(self,isim,yazar,tur,yayınevi,sayfa_sayısı,adet):
        cursor.execute("Insert into kitaplık Values(?,?,?,?,?,?)",(isim,yazar,tur,yayınevi,sayfa_sayısı,adet))
        con.commit() #Kitaplık tablosuna kitap ekler
    def kitap_sil(self,isim):
        cursor.execute("Delete From kitaplık where İsim=?",(isim,))
        con.commit() #kitaplık tablosundan kitap siler.
    def yazar_tara(self,yazar):
        cursor.execute("Select * from kitaplık where Yazar=?",(yazar,))
        liste=cursor.fetchall() #Seçilen yazara göre arama yapar.
        return liste
    def kitap_tara(self,isim):
        cursor.execute("Select * From kitaplık where İsim=?",(isim.capitalize(),))
        liste=cursor.fetchall() #Seçilen bir kitabı arar.
        return liste
    def yayinevi_guncelle(self,yeni,isim):
        cursor.execute("Update kitaplık set Yayınevi=? where İsim=?",(yeni,isim))
        con.commit()  #Seçilen kitabın yayınevini günceller.
    def yayinevi_tara(self,yayinevi):
        cursor.execute("Select * From kitaplık where Yayınevi=?",(yayinevi,))
        liste=cursor.fetchall() #Kitaplık tablosunda yayınevine göre tarama yapar.
        return liste
    def kitap_turu_tara(self,tur):
        cursor.execute("Select * from kitaplık where Tür=?",(tur,))
        liste=cursor.fetchall() #Seçilen bir kitap türüne göre tarama yapar..
        return liste
    def kitaplik_goruntule(self):
        cursor.execute("Select * From kitaplık")
        liste=cursor.fetchall()#Kitaplıktaki tüm kitapları döner.
        return liste
    def kitap_odunc_ver(self,kitap_ismi,yayinevi,yazar,isim,adres,telefonno):
        an=datetime.datetime.now()#Ödünç_Verilenler tablosuna kitap ekler.
        tarih=datetime.datetime.strftime(an, '%d %B %Y %X')
        odunc_verme_suresi=datetime.timedelta(days=30)
        son_tarih=datetime.datetime.strftime(datetime.datetime.now() + odunc_verme_suresi,'%d %B %Y %X')
        cursor.execute("Insert into Ödünç_Verilenler Values(?,?,?,?,?,?,?,?)",(kitap_ismi,yayinevi,yazar,isim,adres,telefonno,tarih,son_tarih))
        con.commit()
    def kitabi_geri_teslim_al(self,kitap_ismi,isim):
        cursor.execute("Delete From Ödünç_Verilenler where Kitap_İsmi=? and Ödünç_Alanın_İsmi=?",(kitap_ismi,isim))    
        con.commit()#Ödünç verilen kitap geri alınır. Kitap Ödünç_Verilenler tablosundan silinir.
    def odunc_alinan_kitap_sayisi(self):
        cursor.execute("Select * from Ödünç_Verilenler")
        liste=cursor.fetchall()#Ödünç verilen toplam kitap sayısını döner.
        return len(liste)
    def odunc_alinan__kitap_isim_tara(self,isim):
        cursor.execute("Select * from Ödünç_Verilenler where Kitap_İsmi=?",(isim,))
        liste=cursor.fetchall()#Ödünç alınan kitaplarda kitap taraması yapar.
        return liste
    def odunc_alinan_isim_tara(self,isim):
        cursor.execute("Select * From Ödünç_Verilenler where Ödünç_Alanın_İsmi=?",(isim,))#Ödünç verilen kitaplarda ödünç alan kişiye göre
        return liste                                                                               #kitap taraması yapar.
    def odunc_alinan_yayinevi_tara(self,yayinevi):
        cursor.execute("Select * From Ödünç_Verilenler where Yayınevi=?",(yayinevi,))
        liste=cursor.fetchall()#Ödünç verilen kitaplarda yayınevine göre kitap taraması yapar.
        return liste


print("""
      ****************************************
      KÜTÜPHANE UYGULAMASI
      
      İşlemler:
        1-Kitap Tara
            A-İsme Göre
            B-Yazara Göre
            C-Türe Göre
            D-Yayınevine Göre
        2-Kitap Ekle
        3-Kitap Sil
        4-Kitaplık Güncelleme
            A-Yayınevi Güncelle
        5-Toplam Kitap Sayısını Görüntüle
        6-Kitap Ödünç Verme
        7-Kitap Geri Teslim Alma
        8-Ödünç Verilen Toplam Kitap Sayısı
        9-Ödünç Verilenlerde Kitap Tara
            A-Kitap İsmine Göre
            B-Ödünç Alana Göre
            C-Yazara Göre
            D-Yayınevine Göre
       
      
      
        0- Programdan Çıkış Yap
        ****************************************
      """)
sonuc_yok="Aramaya uygun sonuç bulunamadı."
hata="Bir şeyler ters gitti."
kitaplık=Kütüphane()
kitaplık.tablo_olustur()    
kitaplık.tablo_olustur2()

while 1:
    try:
     islem=int(input("İşlem No:"))
    except ValueError:
        print("Geçerli bir İşlem No. giriniz!")
    except:
        print(hata)
    
    match islem:
        case 0:
            print("Programdan çıkış yapılıyor...")
            sleep(1)
            break
        case 1:
            try:
                islem_2=input("Tarama Ölçütü:")
            except:
                print(hata)
            match islem_2.upper():
                case "A":
                    kitap_ismi=input("Kitap İsmi:")
                    liste=kitaplık.kitap_tara(kitap_ismi.capitalize())
                    print("Tarama yapılıyor...")
                    sleep(1)
                    if (not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
                case "B":
                    yazar=input("Yazarın İsmi:")
                    liste=kitaplık.yazar_tara(yazar.capitalize())
                    print("Tarama yapılıyor...")
                    sleep(1)
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
                case "C":
                    tur=input("Kitap Türü:")
                    liste=kitaplık.kitap_turu_tara(tur.capitalize())
                    print("Tarama yapılıyor...")
                    sleep(1)
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
                case "D":
                    yayinevi=input("Yayınevi:")
                    liste=kitaplık.yayinevi_tara(yayinevi.capitalize())
                    print("Tarama yapılıyor...")
                    sleep(1)
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
        case 2:
            try:
                isim=input("İsim:")
                yazar=input("Yazar:")
                tur=input("Tür:")
                yayinevi=input("Yayınevi:")
                sayfa=int(input("Sayfa Sayısı:"))
                adet=int(input("Adet:"))
            except:
                print(hata)
            kitaplık.kitap_ekle(isim.capitalize(),yazar.capitalize(),tur.capitalize(),yayinevi.capitalize(),sayfa,adet)
            print("İşlem başarılı.")
        case 3:
            isim=input("İsim:")
            try:
                kitaplık.kitap_sil(isim.capitalize())
                print("İşlem başarılı.")
            except:
                print(hata)
        case 4:
            islem2=input("Güncellenecek Özellik: ")
            if (islem2.upper()=="A"):
                kitap_ismi=input("Kitabın ismi: ")
                kitap=kitaplık.kitap_tara(kitap_ismi.capitalize())
                if(kitap):
                    yeni=input("Yeni yayınevinin ismi: ")
                    kitaplık.yayinevi_guncelle(yeni.capitalize(),kitap_ismi.capitalize())
                    print("İşlem başarılı.")
                else:
                    print("Böyle bir kitap yok.")
            else:
                print("Geçerli bir değer giriniz.")
        case 5:
            print(kitaplık.__len__())
        case 6:
            kitap_isim=input("Kitap İsmi:")
            yayinevi=input("Yayınevi:")
            yazar=input("Yazar:")
            isim=input("Ödünç Alanın İsmi:")
            adres=input("Adresi:")
            telefon=input("Telefon Numarası:")
            kitap=kitaplık.kitap_tara(kitap_isim.capitalize())
            if(kitap):
                kitaplık.kitap_odunc_ver(kitap_isim.capitalize(),yayinevi.capitalize(),yazar.capitalize(),isim.capitalize(),adres.capitalize(),telefon)
            else:
                print("Kitap bulunamadı.")
        case 7:
            kitap_ismi=input("Kitap ismi:")
            isim=input("Ödünç alanın ismi:")
            kitap=cursor.execute("Select * From Ödünç_Verilenler where Kitap_İsmi=? and Ödünç_Alanın_İsmi=?",(kitap_ismi.capitalize(),isim.capitalize()))
            if(kitap):
                kitaplık.kitabi_geri_teslim_al(kitap_ismi.capitalize(),isim.capitalize())
                print("işlem başarılı.")
            else:
                print("Kitap Bulunamadı.")
        case 8:
            print(kitaplık.odunc_alinan_kitap_sayisi())
        case 9:
            islem2=input("Arama Ölçütü:")
            match islem2.upper():
                case "A":
                    isim=input("Kitap ismi:")
                    liste=kitaplık.odunc_alinan__kitap_isim_tara(isim.capitalize())
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
                case "B":
                    isim=input("Ödünç alanın ismi: ")
                    liste=kitaplık.odunc_alinan_isim_tara(isim.capitalize())
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
                case "C":
                    yazar=input("Yazarın ismi: ")
                    liste=kitaplık.odunc_alinan_yazar_tara(yazar.capitalize())
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
                case "D":
                    yayinevi=input("Yayınevi: ")
                    liste=kitaplık.odunc_alinan_yayinevi_tara(yayinevi.capitalize())
                    if(not liste):
                        print(sonuc_yok)
                    else:
                        for kitap in liste:
                            for i in kitap:
                                print(i)
                            print("***********************")
con.close()   
                        
                                
                                        
                    





