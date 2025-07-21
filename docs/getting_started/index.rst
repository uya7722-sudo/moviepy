# Skrip Python untuk menyusun video "Perjalanan Gibran" secara otomatis
# Gunakan library moviepy (pip install moviepy)

from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

# Load video clips (gantilah dengan nama file sebenarnya)
bayi = VideoFileClip("gibran_bayi.mp4").subclip(0, 10)  # 10 detik pertama
besar = VideoFileClip("gibran_besar.mp4").subclip(0, 10)

# Load audio background
musik = AudioFileClip("musik_pop_santai.mp3").volumex(0.5)

# Daftar narasi teks dan waktunya
narasi = [
    ("Setiap langkah kecil ini adalah awal dari kisah besar...", 0),
    ("Hari itu, Gibran hadir membawa tawa kecil ke dunia kami...", 4),
    ("Tangisnya... senyumnya... mengisi hari-hari kami dengan cinta.", 8),
    ("Kini ia tumbuh, belajar, dan melihat dunia dengan mata penuh harapan...", 12),
    ("Terima kasih, Gibran... telah menjadi cahaya dalam hidup kami.", 16)
]

# Buat teks overlay
teks_klip = []
for isi, start in narasi:
    teks = TextClip(isi, fontsize=40, font='Arial', color='white', bg_color='transparent', method='caption', size=(720, None))
    teks = teks.set_start(start).set_duration(4).set_position(('center', 'bottom'))
    teks_klip.append(teks)

# Gabungkan video
gabungan = concatenate_videoclips([bayi, besar])
video_final = CompositeVideoClip([gabungan, *teks_klip])

# Tambahkan musik
video_final = video_final.set_audio(musik.set_duration(video_final.duration))

# Simpan video akhir
video_final.write_videofile("perjalanan_gibran_final.mp4", codec="libx264", audio_codec="aac")
