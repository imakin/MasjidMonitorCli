
class Const(object):
	patern_slideshow_folder = "shows/\d{2}[\.:]{1}\d{2}-\d{2}[\.:]{1}\d{2}-[01]{7}" #regex patern
	patern_slideshow_fullpath = "shows/\d{2}[\.:]{1}\d{2}-\d{2}[\.:]{1}\d{2}-[01]{7}/\d+_\d+\.[a-zA-Z0-9]+" #regex patern
	image_header_format = "data:image/{};base64,{}"
	slideshow_dir = "shows"
	slideshow_subdir_format = "shows/{}"

	months = [0, "januari", "februari", "maret", "april", "mei", "juni", "juli",
	"agustus", "september", "oktober", "november", "desember"]
	
	jumat_day_of_the_week = 4 #in datetime.datetime.now().weekday(), jumat value is 4
	
	@staticmethod
	def get_month(month_pos):
		"""
		get month with month_pos positive value and value will be mod-ed by 12
		1=januari
		2=februari
		12=desember
		0=desember
		"""
		months = ["desember", "januari", "februari", "maret", "april", "mei", "juni", "juli",
		"agustus", "september", "oktober", "november", "desember"]
		return months[month_pos%12]
		
		

	prayer_time_with_jamaat = [
			"maghrib",
			"shubuh",
			"ashr",
			"isya",
			"dzuhur"
		]
	prayer_name = {
		"terbit":"terbit",
		"isyraq":"terbit",
		"syuruq":"terbit",
		"shubuh":"shubuh",
		"dzuhur":"dzuhur",
		"jum'at":"jum'at",
		"jumat":"jum'at",
		"ashr":"ashr",
		"ashar":"ashr",
		"maghrib":"maghrib",
		"isya":"isya",
	}