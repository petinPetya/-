import os
import pandas as pd
import psycopg2

users: set = set()
profiles: dict = dict()

sroki = {
    "Статья 105": 8,
    "Статья 106": 4,
    "Статья 107": 2,
    "Статья 108": 2,
    "Статья 109": 2,
    "Статья 110": 2,
    "Статья 111": 5,
    "Статья 112": 3,
    "Статья 113": 2,
    "Статья 114": 1,
    "Статья 115": 2,
    "Статья 116": 2,
    "Статья 117": 3,
    "Статья 118": 1,
    "Статья 119": 2,
    "Статья 120": 2,
    "Статья 121": 2,
    "Статья 122": 1,
    "Статья 123": 3,
    "Статья 124": 3,
    "Статья 125": 1,
    "Статья 126": 6,
    "Статья 127": 2,
    "Статья 127.1": 4,
    "Статья 127.2": 5,
    "Статья 128": 3,
    "Статья 128.1": 2,
    "Статья 129": 1,
    "Статья 130": 0,
    "Статья 131": 7,
    "Статья 132": 6,
    "Статья 133": 3,
    "Статья 134": 3,
    "Статья 135": 3,
    "Статья 136": 2,
    "Статья 137": 2,
    "Статья 138": 1,
    "Статья 138.1": 4,
    "Статья 139": 2,
    "Статья 140": 2,
    "Статья 141": 2,
    "Статья 141.1": 3,
    "Статья 142": 2,
    "Статья 142.1": 3,
    "Статья 143": 1,
    "Статья 144": 2,
    "Статья 145": 2,
    "Статья 145.1": 1,
    "Статья 146": 2,
    "Статья 147": 2,
    "Статья 148": 1,
    "Статья 149": 3,
    "Статья 150": 5,
    "Статья 151": 3,
    "Статья 152": 4,
    "Статья 153": 3,
    "Статья 154": 1,
    "Статья 155": 2,
    "Статья 156": 3,
    "Статья 157": 1,
    "Статья 158": 2,
    "Статья 159": 3,
    "Статья 160": 2,
    "Статья 161": 2,
    "Статья 162": 4,
    "Статья 163": 3,
    "Статья 164": 6,
    "Статья 165": 2,
    "Статья 166": 2,
    "Статья 167": 2,
    "Статья 168": 1,
    "Статья 169": 2,
    "Статья 170": 2,
    "Статья 170.1": 3,
    "Статья 170.2": 3,
    "Статья 171": 3,
    "Статья 171.1": 5,
    "Статья 171.2": 4,
    "Статья 171.3": 2,
    "Статья 171.4": 3,
    "Статья 172": 3,
    "Статья 172.1": 4,
    "Статья 172.2": 4,
    "Статья 172.3": 3,
    "Статья 173": 1,
    "Статья 173.1": 3,
    "Статья 173.2": 3,
    "Статья 174": 3,
    "Статья 174.1": 4,
    "Статья 175": 3,
    "Статья 178": 5,
    "Статья 179": 2,
    "Статья 180": 2,
    "Статья 181": 3,
    "Статья 183": 4,
    "Статья 184": 3,
    "Статья 185": 3,
    "Статья 185.1": 5,
    "Статья 185.2": 4,
    "Статья 185.3": 4,
    "Статья 185.4": 3,
    "Статья 185.5": 3,
    "Статья 185.6": 2,
    "Статья 186": 5,
    "Статья 187": 4,
    "Статья 188": 4,
    "Статья 189": 2,
    "Статья 190": 3,
    "Статья 191": 5,
    "Статья 191.1": 3,
    "Статья 192": 3,
    "Статья 193": 4,
    "Статья 193.1": 5,
    "Статья 194": 3,
    "Статья 195": 3,
    "Статья 196": 4,
    "Статья 197": 3,
    "Статья 198": 2,
    "Статья 199": 3,
    "Статья 199.1": 2,
    "Статья 199.2": 3,
    "Статья 200": 2,
    "Статья 201": 3,
    "Статья 202": 4,
    "Статья 203": 5,
    "Статья 204": 3,
    "Статья 205": 10,
    "Статья 205.1": 8,
    "Статья 205.2": 6,
    "Статья 205.3": 5,
    "Статья 205.4": 6,
    "Статья 205.5": 5,
    "Статья 206": 8,
    "Статья 207": 5,
    "Статья 208": 10,
    "Статья 209": 10,
    "Статья 210": 10,
    "Статья 211": 8,
    "Статья 212": 5,
    "Статья 213": 5,
    "Статья 214": 3,
    "Статья 215": 4,
    "Статья 215.1": 5,
    "Статья 215.2": 5,
    "Статья 215.3": 6,
    "Статья 216": 3,
    "Статья 217": 4,
    "Статья 218": 4,
    "Статья 219": 4,
    "Статья 220": 5,
    "Статья 221": 5,
    "Статья 222": 5,
    "Статья 223": 5,
    "Статья 224": 4,
    "Статья 225": 4,
    "Статья 226": 6,
    "Статья 226.1": 8,
    "Статья 227": 6,
    "Статья 228": 5,
    "Статья 228.1": 8,
    "Статья 228.2": 5,
    "Статья 228.3": 5,
    "Статья 228.4": 5,
    "Статья 229": 7,
    "Статья 229.1": 8,
    "Статья 230": 4,
    "Статья 230.1": 5,
    "Статья 231": 3,
    "Статья 232": 5,
    "Статья 233": 4,
    "Статья 234": 4,
    "Статья 234.1": 5,
    "Статья 235": 3,
    "Статья 236": 4,
    "Статья 237": 4,
    "Статья 238": 4,
    "Статья 238.1": 5,
    "Статья 239": 3,
    "Статья 240": 4,
    "Статья 241": 5,
    "Статья 242": 5,
    "Статья 242.1": 6,
    "Статья 242.2": 5,
    "Статья 243": 4,
    "Статья 243.1": 5,
    "Статья 243.2": 5,
    "Статья 244": 4,
    "Статья 245": 3,
    "Статья 246": 3,
    "Статья 247": 4,
    "Статья 248": 4,
    "Статья 249": 3,
    "Статья 250": 3,
    "Статья 251": 5,
    "Статья 252": 3,
    "Статья 253": 3,
    "Статья 254": 6,
    "Статья 255": 2,
    "Статья 256": 10,
    "Статья 257": 3,
    "Статья 258": 5,
    "Статья 259": 5,
    "Статья 260": 7,
    "Статья 261": 7,
    "Статья 262": 3,
    "Статья 263": 10,
    "Статья 264": 2,
    "Статья 265": 7,
    "Статья 266": 10,
    "Статья 267": 2,
    "Статья 268": 3,
    "Статья 269": 5,
    "Статья 270": 5,
    "Статья 271": 5,
    "Статья 272": 10,
    "Статья 273": 10,
    "Статья 274": 2,
    "Статья 275": 12,
    "Статья 276": 2,
    "Статья 277": 5,
    "Статья 278": 12,
    "Статья 279": 12,
    "Статья 280": 3,
    "Статья 281": 3,
    "Статья 282": 5,
    "Статья 283": 5,
    "Статья 284": 5,
    "Статья 285": 3,
    "Статья 286": 10,
    "Статья 287": 5,
    "Статья 288": 5,
    "Статья 289": 6,
    "Статья 290": 12,
    "Статья 291": 7,
    "Статья 292": 6,
    "Статья 293": 7,
    "Статья 294": 3,
    "Статья 295": 6,
    "Статья 296": 3,
    "Статья 297": 5,
    "Статья 298": 6,
    "Статья 299": 3,
    "Статья 300": 7,
    "Статья 301": 5,
    "Статья 302": 15,
    "Статья 303": 7,
    "Статья 304": 6,
    "Статья 305": 5,
    "Статья 306": 2,
    "Статья 307": 3,
    "Статья 308": 2,
    "Статья 309": 2,
    "Статья 310": 7,
    "Статья 311": 10,
    "Статья 312": 3,
    "Статья 313": 5,
    "Статья 314": 2,
    "Статья 315": 3,
    "Статья 316": 6,
    "Статья 317": 2,
    "Статья 318": 2,
    "Статья 319": 2,
    "Статья 320": 3,
    "Статья 321": 3,
    "Статья 322": 5,
    "Статья 323": 5,
    "Статья 324": 7,
    "Статья 325": 3,
    "Статья 326": 4,
    "Статья 327": 10,
    "Статья 328": 7,
    "Статья 329": 3,
    "Статья 330": 3,
    "Статья 331": 2,
    "Статья 332": 3,
    "Статья 333": 3,
    "Статья 334": 3,
    "Статья 335": 3,
    "Статья 336": 3,
    "Статья 337": 3,
    "Статья 338": 5,
    "Статья 339": 2,
    "Статья 340": 3,
    "Статья 341": 2,
    "Статья 342": 5,
    "Статья 343": 3,
    "Статья 344": 3,
    "Статья 345": 5,
    "Статья 346": 3,
    "Статья 347": 3,
    "Статья 348": 4,
    "Статья 349": 3,
    "Статья 350": 3,
    "Статья 351": 3,
    "Статья 352": 8,
    "Статья 353": 7,
    "Статья 354": 3,
    "Статья 355": 2,
    "Статья 356": 3,
    "Статья 357": 3,
    "Статья 358": 3,
    "Статья 359": 3,
    "Статья 360": 6,
    "Статья 361": 12,
}

df = pd.DataFrame.from_dict(profiles)