#!/usr/bin/python3

import sys, os, csv

BOM_DIR = '../bom'
HEADER_ROW = ['Description', 'Item Type', 'Janelia Part #', 'Manufacturer',
                'Manufacturer Part #', 'Vendor', 'Vendor Part #',
                'Quantity Per SubAssy']


def prompt_for_positive_integer(prompt):
    valid = False
    while not valid:
        n_raw = input(prompt)
        try:
            n = int(n_raw)
            if (n < 0):
                raise ValueError
            valid = True
        except ValueError:
            print('invalid input: please enter an integer >= 0')
    return n


def add_subAssy_to_bom(subAssy_filename, bom, num_assys):

    """
    subAssy_filename is the path to the subAssy bom CSV
    bom is the dict you wish to add to
    num_assys is the number of subAssy's you wish to add
    """

    with open(subAssy_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        if header != HEADER_ROW:
            print('%s has inconsistent header row. aborting.', subAssy_filename)
            sys.exit(1)
        next(reader)    # skip spacer row
        for row in reader:
            h = hash(tuple(row[:7]))
            if h in bom.keys():
                row_old = bom[h]
                quantity_old = int(row_old[7])
                quantity_new = int(row[7])
                bom[h][7] = str(quantity_old + quantity_new * num_assys)
            else:
                bom[h] = row


def main(test=False):

    # get nbases, narcs, nprobes etc. (or default if test)
    if not test:

        # bases
        nbases = prompt_for_positive_integer('How many Bases? ')
        print()

        # arcs
        narcs = prompt_for_positive_integer('How many Arcs? ')
        print()

        # probe modules
        nprobes = prompt_for_positive_integer('How many Probes? ')
        print()

        # camera modules
        ncameras = prompt_for_positive_integer('How many Camera Modules? ')
        print()

        # laser modules
        nlasers = prompt_for_positive_integer('How many Laser Modules? ')
        print()

        # arc sliders
        valid = False
        while not valid:
            nsliders_raw = input('Auto-calculate Arc Sliders (y)? Or enter '
                                    'quantity manually (n)? ')
            if nsliders_raw == 'y':
                nsliders = nprobes + ncameras + nlasers
                valid = True
            elif nsliders_raw == 'n':
                nsliders = prompt_for_positive_integer('How many Arc Sliders? ')
                valid = True
        print()

        # maintenance stands
        nstands = prompt_for_positive_integer('How many Maintenance Stands? ')
        print()

    else:

        # default config
        nbases = 1
        narcs = 3
        nprobes = 7
        ncameras = 3
        nlasers = 1
        nsliders = 11
        nstands = 2

    # print summary
    print('Summary:')
    print('    %dx Base%s' % (nbases, '' if nbases==1 else 's'))
    print('    %dx Arc%s' % (narcs, '' if narcs==1 else 's'))
    print('    %dx Probe Module%s' % (nprobes, '' if nprobes==1 else 's'))
    print('    %dx Camera Module%s' % (ncameras, '' if ncameras==1 else 's'))
    print('    %dx Laser Module%s' % (nlasers, '' if nlasers==1 else 's'))
    print('    %dx Arc Slider%s' % (nsliders, '' if nsliders==1 else 's'))
    print('    %dx Maintenance Stand%s' % (nstands, '' if nstands==1 else 's'))
    print()

    # concatenate subAssys into bom_total
    bom_total = dict()
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_base.csv'),
                        bom_total, nbases)
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_arc.csv'),
                        bom_total, narcs)
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_probeModule.csv'),
                        bom_total, nprobes)
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_cameraModule.csv'),
                        bom_total, ncameras)
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_laserModule.csv'),
                        bom_total, nlasers)
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_arcSlider.csv'),
                        bom_total, nsliders)
    add_subAssy_to_bom(os.path.join(BOM_DIR, 'bom_subAssy_maintenanceStand.csv'),
                        bom_total, nstands)

    # output bom_total as CSV
    filename_output = input('Enter a filename for the output CSV (including '
                            'extension): ')
    with open(filename_output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(HEADER_ROW)
        writer.writerow(['',''])
        for row in bom_total.values():
            writer.writerow(row)
    print('Wrote total BOM to %s' % filename_output)


if __name__ == '__main__':

    if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
        main(True)
    else:
        main(False)

