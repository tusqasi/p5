#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""3D geometry class for p5py
"""

import numpy as np
import math

class Geometry:
	def __init__(self, detail_x=None, detail_y=None):
		self.vertices = []

		self.line_vertices = []

		self.line_normals = []

		self.vertex_normals = []

		self.faces = []

		self.uvs = []
		# a 2D array containing edge connectivity pattern for create line vertices
		# based on faces for most objects
		self.edges = []
		self.detail_x = detail_x if detail_x else 1
		self.detail_y = detail_y if detail_y else 1

		self.stroke_indices = []

	def reset(self):
		self.vertices = []
		self.line_vertices = []
		self.line_normals = []
		self.vertex_normals = []
		self.faces = []
		self.uvs = []
		self.edges = []

	def compute_faces(self):
		self.faces = []
		slice_ount = self.detail_x + 1
		for i in range(self.detail_y):
			for j in range(self.detail_x):
				a = i * sliceCount + j
				b = i * sliceCount + j + 1
				c = (i + 1) * sliceCount + j + 1
				d = (i + 1) * sliceCount + j
				self.faces.append([a, b, d])
				self.faces.append([d, b, c])

	def make_triangle_edges(self):
		self.edges = []
		for j in range(len(self.faces)):
			self.edges.append([self.faces[j][0], self.faces[j][1]])
			self.edges.append([self.faces[j][1], self.faces[j][2]])
			self.edges.append([self.faces[j][2], self.faces[j][0]])

	def get_face_normal(self, faceId):
		face = self.faces[faceId]
		vA = np.array(self.vertices[face[0]])
		vB = np.array(self.vertices[face[1]])
		vC = np.array(self.vertices[face[2]])
		ab = vB - vA
		ac = vC - vA
		n = np.cross(ab, ac)
		ln = np.linalg.norm(n)

		sinAlpha = ln / (np.linalg.norm(ab) * np.linalg.norm(ac))
		if sinAlpha > 1: 
			sinAlpha = 1

		return n*math.sin(sinAlpha)/ln

	def compute_normals(self):
		self.vertex_normals = []
		for iv in range(len(self.vertices)):
			self.vertex_normals.append([])

		for f in range(len(self.faces)):
			face = self.faces[f]
			face_normal = self.get_face_normal(f)

			for fv in range(3):
				vertex_index = face[fv]
				self.vertex_normals[vertex_index].append(face_normal)

		for iv in range(len(self.vertices)):
			self.vertex_normals[iv] = self.vertex_normals[iv]/np.linalg.norm(self.vertex_normals[iv])

	def edges_to_vertices(self):
		self.line_vertices = []
		self.line_normals = []

		for i in range(len(self.edges)):
			begin = self.vertices[self.edges[i][0]]
			end = self.vertices[self.edges[i][1]]

			direction = np.linalg.norm(end - begin)


