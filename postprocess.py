import numpy as np
import getLines
from textblock import TextBlock

def seperate_sets(lines):
# Fixes lines so that each point belongs to only 1 line

    processed_lines = []
    # Remove points
    while lines:
        
        # If lines are still good enough
        best_line = max(lines, key=lambda x: x[0])
        if best_line[0] > 3:

            # Get rid of the best line, and remove all of its points from
            # every other line
            processed_lines += [best_line]
            new_lines = []
            lines.remove(best_line)
            for line in lines:

                # Keep this line's points ONLY if they are not in best_line
                new_points = []
                for point in line[2]:
                    # Assume its unique until a match is found
                    is_unique = True
                    for processed_point in best_line[2]:

                        if np.array_equal( point[0], processed_point[0]):
                            is_unique = False
                            break

                    if is_unique: new_points += [point]

                # Add this line if it still contains points
                if new_points: new_lines += [(line[0],line[1], new_points)]

            lines = new_lines

            # Calculate new quality for each line
            for line in lines:

                linebox = [ [line[1][0]]*2, [line[1][1]]*2 ]
                qual, _ = getLines.quality( linebox, line[2] )
                line = (qual,line[1],line[2])

        else: break

    return processed_lines

def adopt_orphaned_chars(lines, points):
# Add all points that don't belong to a line to the nearest line

    line_points = [ line[2] for line in lines ]
    points = [ point for point in points if point not in line_points ]

def merge_lines(lines, eps, d):
# Output Text_blocks from lines

    text_blocks = []
    for line in lines:

        # Create a bounding rectangle
        rects = [rect[1] for rect in line[2]]
        x = min( rects, key=lambda point: point.x ).x
        w = max( rects, key=lambda point: point.x+point.w ).x - x
        y = int(np.median([point.y for point in rects])-eps)
        h = int(np.median([point.y+point.h for point in rects])+d) - y
#        y = min( rects, key=lambda point: point.y ).y
#        h = max( rects, key=lambda point: point.y+point.h ).x - y

        # Add this rectangle
        text_blocks += [TextBlock((x,y),(x+w,y+h))]

    return text_blocks

def post_process(text_lines, points, eps, d):

    text_lines = seperate_sets(text_lines)
#    adopt_orphaned_chars(lines,points)
    text_blocks = merge_lines(text_lines, eps, d)
    return text_lines, text_blocks
