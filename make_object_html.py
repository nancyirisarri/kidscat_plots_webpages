'''
For each of the KiDS objects with plots, make an HTML file containing
the statistics of the KiDS object.
'''

from astro.main.SourceList import SourceList
from common.log.Comment import Comment
from common.log.Message import Message

from astro.experimental.kids.plot_kidscat_new import KidsCat
from astro.experimental.kids.plot_kidscat_new import PlotKidsCat

import numpy as np
import traceback
import subprocess

def find_sourcelists_by_comment(comment):
    query = Comment.content == comment
    sls = [SourceList(object_id=c.db_object_id) for c in query]
    Message("%i SourceLists found" % len(sls))
    return sls

def get_stats(sourcelist):
    '''Access the KiDS-CAT values that are ingested in AWE, which are in
    Comment objects. See
    http://wiki.astro-wise.org/projects:kids:data_deliveries:kids-eso-dr1:sourcelists#statistics

    Return a dictionary with the values we want to compare.
    '''
    comment = (
      (Comment.db_object_id == sourcelist.object_id.binary()) &\
      (Comment.content.like("*completeness*"))
    )[0]
    stats1 = eval(comment.content)

    comment = (
      (Comment.db_object_id == sourcelist.object_id.binary()) &\
      Comment.content.like("*ellipticity*")
    ).max('creation_date')
    stats2 = eval(comment.content)

    stats = {
      'fwhm_mean': stats1['fwhm']['fwhm'],
      'fwhm_sigma': stats1['fwhm']['sigma'],
      'elall': stats2['ellipticity']['ellipticity_selected_stars'],
      'elss': stats2['ellipticity']['ellipticity_sure_stars'],
      'magsat': stats2['abmagsat']['mag_saturation'],
      'mcompl': stats1['completeness']['completeness'],
      'mlim_sn5': stats1['mlim'][0]['MLIM'],
      'mlim_sn10': stats1['mlim'][1]['MLIM'],
      'mlim_sn15': stats1['mlim'][2]['MLIM']
    }

    return stats

def do_all(sls):

    #filename_html = 'kidscat-latest.html'
    try:
        subprocess.call('rm -f %s' % filename_html, shell=True)
    except:
        traceback.print_exc()

    for i in range(len(sls)):
        sourcelist = sls[i]

        stats = get_stats(sourcelist)

        filename_catalog = sourcelist.OBJECT
        sl_filter = sourcelist.filter.name
        sl_filename = sourcelist.filename

        filename_html = '%s_%s.html' %\
          (
          filename_catalog.replace('KIDS', 'KiDS').replace('KiDS_', 'KiDS_INTDR3_'), 
          sl_filter[5]
          )

        catalog = KidsCat(
          filename_catalog, sl_filter, sl_filename
        )
        catalog.load_data(filename_catalog)

        plot = PlotKidsCat(
          catalog.find_sourcelist(), catalog.sl_name, catalog.data, catalog.atts
        )
        plot.make(
          'MLIM', do_plot=False
        )

        plot.make(
          'COMPL', do_plot=False
        )

        plot.make(
          'ABMAGSAT', do_plot=False
        )

        calculated = {
          'fwhm_mean': plot.fwhm_mean*0.2,
          'fwhm_sigma': plot.fwhm_sigma*0.2,
          'elall': plot.median_elall,
          'elss': plot.median_elss,
          'magsat': plot.magsat,
          'mcompl': plot.mcompl,
          'mlim_sn5': plot.mlim_sn5,
          'mlim_sn10': plot.mlim_sn10,
          'mlim_sn15': plot.mlim_sn15,
        }

        with open(filename_html, 'a') as fp:
            fp.write('<h2>%s</h2><br>' % sourcelist.filename)
            fp.write('<table width="50%">')
            fp.write('<tr><td>statistic</td><td>error</td><td>calculated</td><td>ingested</td></tr>')

        for key in sorted(stats.keys()):
            error = 100 * (np.abs(calculated[key] - stats[key]) / stats[key])
            if error > 5:
                with open(filename_html, 'a') as fp:
                    fp.write(
                      '<tr><td><span style="font-weight:bold;">%s</span></td><td><span style="color:red;">%s</span></td><td>%s</td><td>%s</td></tr>' %\
                      (key, error, calculated[key], stats[key])
                    )
            else:
                with open(filename_html, 'a') as fp:
                    fp.write(
                      '<tr><td><span style="font-weight:bold;">%s</span></td><td>%s</td><td>%s</td><td>%s</td></tr>' %\
                      (key, error, calculated[key], stats[key])
                    )

        with open(filename_html, 'a') as fp:
            fp.write('</table><br><br>')

        try:
            subprocess.call(
              'rsync /net/virgo01/data/users/irisarri/kidscat/%s irisarri@schipbeek.strw.leidenuniv.nl:/home/irisarri/public_html/' %\
              filename_html, shell=True
            )
        except:
            traceback.print_exc()

if __name__ == '__main__':

    obs = [
      'KIDS_141.0_-0.5', 'KIDS_140.0_-1.5', 'KIDS_139.4_2.5', 
      'KIDS_174.0_0.5', 'KIDS_32.6_-31.2'
    ]

    sls = []

    for i in obs:
        for j in 'OCAM_i_SDSS', 'OCAM_u_SDSS', 'OCAM_r_SDSS',\
          'OCAM_g_SDSS':
            sl = (SourceList.OBJECT == i) &\
              (SourceList.filter.name == j) &\
              (SourceList.filename.like('*KCv1.6_INTDR3v4*'))

            if len(sl) == 1:
                sls.append(sl[0])
            else:
                print i, j
                exit()

    do_all(sls)
