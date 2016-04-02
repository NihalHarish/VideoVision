# Place this file in the folder 'VIRAT Ground Dataset' ie. the folder that contains 'annotations'
import cv2
import time
files = ['VIRAT_S_000200_00_000100_000171.mp4'] #add the names of files you wish to annotate
for fname in files:
    file_name = "annotations/" + fname.split(".")[0] + ".viratdata.objects.txt"
    video_name = "videos_original/" + fname

    f = open(file_name, "r")
    flines = f.readlines()
    f.close()
    lines = [flines[0]]
    to_write = []
    for line in flines:
        if line.split(" ")[0] != lines[-1].split(" ")[0]:
            lines.append(line)


    cap = cv2.VideoCapture(video_name)
    currline = 0
    while True:
        if currline == len(lines):
            break
        line = lines[currline]
        oid, dur, frame_num, x, y, w, h, dummy = map(int, line.split(" "))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        flag, frame = cap.read()
        print("*"*50)
        print(line)
        print("*"*50)
        if flag:
            img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
            cv2.imshow('img', img2)
            #cv2.imshow('video', frame)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            cv2.waitKey(1000)
            resp = raw_input("Enter 'colour gender race': ")
            currline += 1
            to_write.append((oid, resp))
        if cv2.waitKey(10) == 27:
            break

    confirm = raw_input("Write to file?(y/n): ")
    write_lines = []
    curr = 0
    if confirm == 'y':
        with open(file_name, 'r') as f:
            for x in f.readlines():
                x = x.strip()
                if (curr < len(to_write) and int(x.split(" ")[0]) == to_write[curr][0]):
                    write_lines.append(' '.join([x, to_write[curr][1], '\n']))
                    curr += 1
                else:
                    write_lines.append(' '.join([x, '\n']))


    with open(file_name, 'w') as f:
        for line in write_lines:
            f.write(line)
