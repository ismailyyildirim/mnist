# -*- coding: utf-8 -*-
"""mnist.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AAyxNYJ-QLAndhXF1QI1VBhCjeUHgLUT

# Kerasta MNİST veri setini yüklemek
"""

from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

"""train_images ve train_labels modelimizin öğrenmek için kullanacağı eğitim veri setini oluşturmaktadır. Modelimiz daga sonra test veri setini oluşturan test_images ve test_labels üzerinde test edilecektir. Görüntüler Numpy dizisi olarak kodlanmış ve etiketler 0 ile 9 arasındaki rakamlardan oluşan birer dizidir. Görüntüler ve etiketler arasında birebir ilişki vardır."""

print("train_images: ",train_images.shape)
print("test_images: ",test_images.shape)

"""Akışımız şu şekilde olacak: Önce sinir ağımızı eğitim veri seti ile besleyeceğiz ve ağımız görüntüüler ile etiketleri eşleştirmeyi öğrenecek. Sonra test_images için ağımızın tahminlerini üretip son olarak test_labels ile ağımızın ürettiği sonuçları aynı olup olmadığını kontrol edeceğiz.
Şimdi ağımızı oluşturuyoruz.

# Ağ Mimarisi
"""

from keras import layers
from keras import models

network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))

"""Derin ağların temel yapı taşı, veri için filtre olarak düşünülebilecek veri işleme modülü olan katmanlardır. Veri katmana ham hali ile girer ve daha kullanışlı bir formda çıkar. Katmanlar kendisini besleyen verilerden problemin çözümünde yardımcı olacak daha anlamlı gösterimler çıkartmaya çalışırlar. Derin öğrenme süreci çoğunlukla basit katmanları üst üste getirerek verinin ilerledikçe daha da artırılmasını sağlayan bir yapıdır. Derin öğrenme, verinin ilerledikçe daha da artırıldığı birbirini takip eden süzgeçlere benzetilebilir. 
Modelimiz, 2 adet birbirini takip eden Dense katmanını içeriyor. İkinci (yani son katmanımız) 10 adet çıktı birimi bulunan ve 10 elemanlı olasılık puanlarını gösteren (toplamları 1) bir diziyi geriye döndürülür. Dizinin her bir elemanı, o anki örneğimizdeki sayının 1'den 10'a kadar hangi sınıfına ait olduğunu gösteren bir olasılık değeridir.

Ağımızın eğitime hazır hale getirmek için 3 şeyi daha derleme adımı olarak almamız gerekiyor:


1.   Kayıp fonksiyonu --- Ağımızın eğitim veri seti üzerinde kendi performansını gözlemlemesi ve böylece kendi kendine doğru yolu bulabilmesi için.
2.   Eniyileme --- Ağımızın girdisi olan veri ile oluşturduğu kaybı performansını bulundurarark kendisini güncelleme mekanizması.
3.   Eğitim ve Test Süresince takip edilecek Metrikler --- Burada biz sadece doğruluğa (doğru sınıflandırılan görüntülerin topam görüntüsü sayısına oranı) odaklanacağız.

# Derleme Adımı
"""

network.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

"""Eğitime başlamadan önce, tüm girdilerimizideki değerleri [0,1] aralığına ölçeklendiriyoruz. Bu aşamadan önce eğitim veri setimizdeki görüntüler (60000, 28, 28) şeklinde bir dizide ve her elemanı uint8 veri tipinde [0, 255] veri aralığında saklanmıştı. Eğitim veri setindeki görüntüleri (60000, 28, 28) float32 veri tipinde 0 ile 1 arasında olacak şekilde düzenliyoruz.

# Girdilerin Hazırlanması
"""

train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

"""Aynı zamanda etiketlerimizi kategorik olarak etiketlememiz gerekiyor.

# Etiketlerin Hazırlanması
"""

from keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

"""Artık eğitime başlayabiliriz. Bunu için Kerasın fit metodunu çağırarak modelimizi eğitim veri setine uyduruyoruz."""

network.fit(train_images, train_labels, epochs=5, batch_size=128)

"""Eğitim süresince iki değer gösteriliyor: Ağın eğitim veri seti üzerindeki kaybı ve doğruluğu.


> Eğitim veri setinde çabucak 0.989 yani %98.9'luk bir doğruluğa ulaştık. Bir de ağımızı test veri seti üzerinde deneyelim:


"""

test_loss, test_acc = network.evaluate(test_images, test_labels)

print('test_acc: ', test_acc)
print('test_loss: ', test_loss)

