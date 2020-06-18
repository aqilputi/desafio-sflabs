import videotransf as vt

transf = vt.VideoTransf("720.avi")

transf.split(10000)

transf.slice(5000, 50000)

transf.append("720.avi")

transf.release()

