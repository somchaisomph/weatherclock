import dash_html_components as html

layout = 	html.Div(id="clock-div",
				className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12",
				children=[
					html.Div(className="relative py-2 sm:max-w-xl sm:mx-auto",
					children=[
					
						html.Div(className="absolute inset-0 bg-gradient-to-r from-cyan-200 to-sky-800 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"),
						html.Div(className="relative px-5 py-5 bg-white shadow-lg sm:rounded-3xl sm:p-20",
							children=[
								html.Div(className="max-w-md mx-auto",
									children=[										
										html.Div(id="title-div",
											className="text-center text-3xl text-blue-900",
											children="Weather Clock"),
										html.Div(className="grid grid-rows-2 gap-1",
											children=[
												html.Div(id="upper-part", 
													className="border bg-gray-100 rounded-lg h-20",
													children=[
														html.Div(className="grid grid-cols-2 p-1 gap-1",
															children=[
																html.Div(id="date-div",
																	className="bg-blue-200 box-border grid grid-rows-3 text-sky-900 rounded-lg text-center",
																	children=[
																		html.Div(id="week-div",children="Mon"),
																		html.Div(id="month-div",children="21 June"),
																		html.Div(id="year-div",children="2021")
																	]),
																html.Div(className="align-middle text-center items-center \
																flex justify-self-center",
																	children=[
																		html.Div(id="time-div",
																			className="text-center text-sky-900 text-4xl",
																			children="15:00:00")
																	])
															])
													]),
												html.Div(id='lower-part',
													className="bg-white text-center rounded-lg h-28",
													children=[
														html.Div(className="grid grid-cols-2",
															children=[
																html.Div(id='cond-div',className="bg-white px-1 py-1 rounded-lg",
																	children=[
																		html.Img(id='cond-img',
																		src="/image/cool.png",width="180",height="180")
																	]),
																html.Div(className="grid grid-cols-2 grid-rows-2 p-1 gap-1 \
																items-center align-middle justify-items-center",
																	children=[
																		html.Div(className="w-20 p-1 border-2 rounded-lg",
																			children=[
																				html.Div(className="font-bold",
																						children=[
																							html.Img(src="/image/warm.png")
																						]),
																				html.Div(id='tmp-val',children="1")
																			]),
																		html.Div(className="w-20 p-1 border-2 rounded-lg",
																			children=[
																				html.Div(className="font-bold",
																					children=[
																						html.Img(src="/image/humidity.png")
																					]),
																				html.Div(id='humid-val',children="1")
																			]),
																		html.Div(className="w-20 p-1 border-2 rounded-lg",
																			children=[
																				html.Div(className="font-bold",
																					children=[
																						html.Img(src="/image/windy.png")
																					]),
																				html.Div(id='wind-val',children="1")
																			]),
																		html.Div(className="w-20 p-1 border-2 rounded-lg grid-cols-2",
																			children=[
																				html.Div(className="font-bold",
																					children=[
																						html.Img(src="/image/rainy.png")
																					]),
																				html.Div(id='rain-val',children="1")
																			])
																	])
															])
													])
											])
									])
							])
					])
				]
			)
	
