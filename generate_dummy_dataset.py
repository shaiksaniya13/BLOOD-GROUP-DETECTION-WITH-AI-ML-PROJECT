import os
import cv2
import numpy as np

groups = ['A', 'B', 'AB', 'O']
for t in ['train', 'test']:
    for g in groups:
        path = f'dataset/{t}/{g}'
        os.makedirs(path, exist_ok=True)
        for i in range(10):
            img = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
            cv2.putText(img, g, (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
            cv2.imwrite(f'{path}/{g}_{i}.jpg', img)
print("✅ Dummy dataset created!")

