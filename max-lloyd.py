import cv2						          # OpenCV library
import matplotlib.pyplot as plt	# Histogram
import bisect					          # Bisect for faster lookup

# Max-Lloyd Algorithm
def quantize(left, right, threshold):
  global pixelFreq, ranges
  pixelSum = sum(pixelFreq[left : right])
  size = right - left
  mean = pixelSum / size
  squaredError = 0
  for value in pixelFreq[left : right]:
    squaredError += abs(mean - value) ** 2
  mse = squaredError / size
  if(mse > threshold):
    mid = (right + left) // 2
    quantize(left, mid, threshold)
    quantize(mid, right, threshold)
  else:
    ranges.append(left)

img = cv2.imread('Image path goes here')
dim = (240, 320)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print('Gambar asli:')
cv2.imshow(img)

print('Gambar grayscale:')
cv2.imshow(grayImg)

# Count frequency of pixel value here
pixelFreq = [0] * 256
for r in range(320):
  for c in range(240):
    pixelFreq[grayImg[r][c]] += 1

# Make histogram data here
histoData = list()
for r in range(320):
  for c in range(240):
    histoData.append(grayImg[r][c])

plt.hist(histoData, bins = 256, range = (-0.5, 255.5))
plt.xlabel('Value')
plt.ylabel('Frekuensi')
plt.show()

# Make quantization ranges
ranges = list()  
quantize(0, 256, 100) # Change threshold value for different results   
print('Banyak level kuantisasi:', len(ranges))

# Make newImg same as grayImg but quantized non-uniformly
newImg = grayImg    # newImg adalah gambar setelah quantization
for r in range(320):
  for c in range(240):
    newImg[r][c] = bisect.bisect(ranges, newImg[r][c])

print('Gambar asli : ')
cv2.imshow(grayImg)

print('Gambar setelah quantization : ')
cv2.imshow(newImg)
