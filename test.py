import videotransf as vt

transf = vt.VideoTransf("videos/1591821600_015.mp4")

transf.video_format = 'avi'

transf.split(10000)

transf.slice(5000, 50000)

transf.append("720.avi")

transf.release()

