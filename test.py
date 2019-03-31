import torch
import numpy as np
from model import C3D
import cv2

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# torch.backends.cudnn.benchmark = True

model_path = '.\\model\\model_epoch12_accuracy_0.9910714285714285.pkl'
def center_crop(frame):
    frame = frame[8:120, 30:142, :]
    return np.array(frame).astype(np.uint8)

def get_all_classes():

    with open('ucf_labels.txt', 'r') as f:
        class_names = f.readlines()
        f.close()
    return class_names


def init_model():
    # init model
    return C3D(num_classes=101,pretrained=True)

    # get the checkpoint
    # checkpoint = torch.load('c3d-pretrained.pth', map_location=lambda storage, loc: storage)

    # load the parameters into the model
    # print(checkpoint)
    # model.load_state_dict(checkpoint['state_dict'])


def read_video(video):
    return cv2.VideoCapture(video)


def main():
    #check the device cpu or gpu
    print("Device being used:", device)
    video = 'v_ApplyLipstick_g04_c02.avi'

    # read all class names into the memory
    class_names = get_all_classes()

    # init model
    # model = C3D(num_classes=101,pretrained=True)
    model = torch.load(model_path)

    #put onto gpu if possible
    model.to(device)

    #???
    # model.train()

    # read video
    cap = cv2.VideoCapture(video)



    ret = True

    clip = []
    while ret:
        #read frame by frame
        ret, frame = cap.read()

        if not ret and frame is None:
            continue
        # resize to the test size
        tmp_ = center_crop(cv2.resize(frame, (171, 128)))

        #seems normalize color
        tmp = tmp_ - np.array([[[90.0, 98.0, 102.0]]])

        clip.append(tmp)
        if len(clip) == 16:
            # 16 * 112 * 112 * 3
            inputs = np.array(clip).astype(np.float32)

            # 1 * 16 * 112 * 112 * 3
            inputs = np.expand_dims(inputs, axis=0)

            # 1 * 3 * 16 * 112 * 112
            inputs = np.transpose(inputs, (0, 4, 1, 2, 3))

            inputs = torch.from_numpy(inputs)

            inputs = torch.autograd.Variable(inputs).to(device)

            #put into model
            outputs = model.forward(inputs)

            # get the probs
            probs = torch.nn.Softmax(dim=1)(outputs)
            # print(probs)

            #get the label index
            label = torch.max(probs, 1)[1].detach().cpu().numpy()[0]

            cv2.putText(frame, class_names[label].split(' ')[-1].strip(), (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 0, 255), 1)
            cv2.putText(frame, "prob: %.4f" % probs[0][label], (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 0, 255), 1)
            clip.pop(0)

        cv2.imshow('result', frame)
        cv2.waitKey(30)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
