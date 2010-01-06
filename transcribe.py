#!/usr/bin/env python

import gtk

import Visualizer
import Pipeline
import Timeline

class Transcribe:
	def __init__(self):
		# create gui
		self.builder = gtk.Builder()
		self.builder.add_from_file("gui.glade")
		self.builder.get_object("rate").set_value(100)

		# create pipeline
		self.pipeline = Pipeline.Pipeline("/home/maxi/Musik/ogg/jamendo_track_401871.ogg")
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
#		bus.connect()

		# create timeline
		self.timeline = Timeline.Timeline(self.pipeline.duration)
		self.builder.get_object("scrolledwindow").add(self.timeline)
		self.timeline.show_all()

		# create fretboard
		self.fretboard = Visualizer.Fretboard(self.pipeline.spectrum)
		self.fretboard.connect_to_bus(bus)
		self.builder.get_object("vbox").pack_start(self.fretboard,expand=False)
		self.fretboard.show_all()

		# connect signals
		self.builder.connect_signals(self)

	def run(self):
		self.builder.get_object("mainwindow").show_all()
		gtk.main()

	# callbacks

	def quit(self, *args):
		gtk.main_quit()

	def insert_text(self,widget):
		self.timeline.mode="insert_text"

	def play(self,widget):
		marker = self.timeline.get_marker()
		rate = self.builder.get_object("rate").get_value()/100.

		if marker:
			self.pipeline.play(rate,start=marker[0],stop=marker[0]+marker[1])

		self.builder.get_object("pause").set_active(False)
		self.builder.get_object("stop").set_sensitive(True)

	def pause(self, widget):
		if widget.get_active():
			self.pipeline.pause()
		else:
			rate = self.builder.get_object("rate").get_value()/100.
			self.pipeline.play()

	def stop(self,widget):
		self.pipeline.pause()
		self.builder.get_object("pause").set_active(False)
		self.builder.get_object("stop").set_sensitive(False)

if __name__=="__main__":
	transcribe = Transcribe()
	transcribe.run()
