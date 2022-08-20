from cell import Cell


def live(cell, cells):
    if cell.health > 100:
        cell.divide(cells)
    elif cell.health > 0:
        gene = cell.dna[cell.gene_pos]
        match gene:
            case gene if 0 <= gene <= 7:
                cell.step(gene)
            case gene if 8 <= gene <= 15:
                # cell.catch(gene)
                pass
            case gene if 16 <= gene <= 23:
                # cell.look(gene)
                pass
            case gene if 24 <= gene <= 31:
                # cell.rotate(gene)
                pass
            case gene if 32 <= gene <= 62:
                cell.gene_jump(gene)
            case 63:
                # cell.photosynthesis(gene)
                pass
        cell.health -= 1
    else:
        cell.is_alive = False


def is_collide(obj, obj_list):
    for current in obj_list:
        if obj.position == current.position and obj is not current:
            return current
    return False


def check_neighbors(obj, obj_list):
    res = []
    for current in obj_list:
        if tuple(x-y for x, y in zip(obj.position, current.position)) in Cell.dirlist:
            res.append([type(current), current.position])
    return res



