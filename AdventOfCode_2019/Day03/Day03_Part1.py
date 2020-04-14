#from collections import defaultdict

filepath = 'Day03/Day03_Input.txt'
data = {}

def main():
    closest = 99999999999
    lines = []
    idx = 0

    with open(filepath) as fp:
        for line in fp:
            lines = line.strip()
            lines = lines.split(",")

            pos = ([0,0])
            data[idx] = {}
            data[idx].setdefault("horizontal", [])
            data[idx].setdefault("vertical", [])

            for l in lines:
                dir = l[0]
                length = int(l[1:])

                if dir == "L":
                    print("L -add horizontal: pos={}, length={}".format(pos, length))

                    pos[0] -= length
                    data[idx]["horizontal"].append([pos[0], pos[1], length])

                    closest = min(closest, checkintersect(idx, "horizontal", pos, length))
                elif dir == "R":
                    print("R -add horizontal: pos={}, length={}".format(pos, length))

                    data[idx]["horizontal"].append([pos[0], pos[1], length])

                    closest = min(closest, checkintersect(idx, "horizontal", pos, length))
                    pos[0] += length
                elif dir == "D":
                    print("D - add vertical: pos={}, length={}".format(pos, length))

                    pos[1] -= length
                    data[idx]["vertical"].append([pos[0], pos[1], length])

                    closest = min(closest, checkintersect(idx, "vertical", pos, length))
                elif dir == "U":
                    print("U - add vertical: pos={}, length={}".format(pos, length))

                    data[idx]["vertical"].append([pos[0], pos[1], length])

                    closest = min(closest, checkintersect(idx, "vertical", pos, length))
                    pos[1] += length

            idx += 1
        print(closest)
        return closest

def checkintersect(idx, dir, pos, length):
    closestintersectpos = 99999999999
    for i in range(0, idx):
        if dir == "horizontal":
            endpos = pos[0] + length
            for value in data[i].get("vertical", []):
                if pos[0] <= value[0] <= endpos:
                    if value[1] <= pos[1] <= value[1] + value[2]:
                        intersectpos = [value[0], pos[1]]
                        closestintersectpos = min(closestintersectpos, abs(intersectpos[0]) + abs(intersectpos[1]))
                        #print("Found {} intersection at {}".format(dir, intersectpos))                        
        elif dir == "vertical":
            endpos = pos[1] + length
            for value in data[i].get("horizontal", []):
                if pos[1] <= value[1] <= endpos:
                    if value[0] <= pos[0] <= value[0] + value[2]:
                        intersectpos = [pos[0], value[1]]
                        closestintersectpos = min(closestintersectpos, abs(intersectpos[0]) + abs(intersectpos[1]))
                        #print("Found {} intersection at {}".format(dir, intersectpos))

    return closestintersectpos


if __name__ == '__main__':
    main()
