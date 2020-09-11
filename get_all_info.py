import re
import datetime
from more_itertools import locate
from operator import itemgetter

f_w = ""
def set_f_w(name_code):
  global f_w
  src = "./result/" + name_code + ".txt"
  f_w = open(src, 'w')

def start_date(sample_raw):
  degreeName = get_info(sample_raw, '"degreeName"')
  if degreeName == None:
    is_education = False
  else:
    is_education = True
  pattern = r'"start".*?},'
  start_date_info = re.findall(pattern, sample_raw)[0]
  number_list = re.findall(r'[0-9]', start_date_info)
  if len(number_list) == 5:
    month = number_list[0]
    year = ""
    for i in range(1, len(number_list)):
      year += number_list[i]
  elif len(number_list) == 6:
    month = number_list[0] + number_list[1]
    year = ""
    for i in range(2, len(number_list)):
      year += number_list[i]
  else:
    #判斷是不是education,是的話raise exception,不是的話回傳year, month
    year = ""
    for i in range(len(number_list)):
      year += number_list[i]
    if is_education:
      raise Exception(year)
    else:
      month = "0"
      return year, month
  return year, month

def end_date(sample_raw):
  degreeName = get_info(sample_raw, '"degreeName"')
  if degreeName == None:
    is_education = False
  else:
    is_education = True
  pattern = r'"end".*?},'
  try:
    end_date_info = re.findall(pattern, sample_raw)[0]
  except:
    date_now = datetime.datetime.now()
    year = date_now.year
    month = date_now.month
    return year, month
  number_list = re.findall(r'[0-9]', end_date_info)
  if len(number_list) == 5:
    month = number_list[0]
    year = ""
    for i in range(1, len(number_list)):
      year += number_list[i]
  elif len(number_list) == 6:
    month = number_list[0] + number_list[1]
    year = ""
    for i in range(2, len(number_list)):
      year += number_list[i]
  else:
    #判斷是不是education,是的話raise exception,不是的話回傳year, month
    year = ""
    for i in range(len(number_list)):
      year += number_list[i]
    if is_education:
      raise Exception(year)
    else:
      month = "0"
      return year, month
  return year, month

def calculate_duration(start_year, start_month, end_year, end_month):
  duration_year = int(end_year) - int(start_year)
  duration_month = int(end_month) - int(start_month)
  if start_month != "0" and end_month != "0":
    duration_total = duration_year * 12 + duration_month + 1
  else:
    duration_total = duration_year * 12 + duration_month
  return duration_total // 12, duration_total % 12

def get_info(sample_raw, info_key):
  pattern = info_key + r'.*?,"'
  try:
    info = re.findall(pattern, sample_raw)[0][len(info_key) + 2:-3]
    if info == "ul":
      return "null"
  except:
    return None
  #能正常顯示換行
  info = info.replace('\\n', '\n').replace('\\t', '\t')
  return info

def show_info(companyName, title, locationName, description, start_year, start_month, end_year, end_month, duration_year, duration_month):
  if companyName != None:
    f_w.write("公司名稱 :" + companyName)
    f_w.write('\n')
  if title != None:
    f_w.write("職位名稱 :" + title)
    f_w.write('\n')
  if locationName != None:
    f_w.write("公司位置 :" + locationName)
    f_w.write('\n')
  if description != None:
    f_w.write("職位描述 :\n" + description.strip(''))
    f_w.write('\n')
  f_w.write("工作期間 :")
  has_month_info = (start_month != "0" and end_month != "0")
  start_year = str(start_year)
  start_month = str(start_month)
  end_year = str(end_year)
  end_month = str(end_month)
  duration_year = str(duration_year)
  duration_month = str(duration_month)
  if int(duration_year)  > 0:
    if int(end_year) == datetime.datetime.now().year and int(end_month) == datetime.datetime.now().month:
      if has_month_info == True:
        output_str = start_year + "年" + start_month + "月 - " + end_year+ "年" + end_month + "月(目前) 共" + duration_year + "年" + duration_month + "月"
      else:
        output_str = start_year + "年" + " - " + end_year + "年(目前) 共" + duration_year + "年"
    else:
      if has_month_info == True:
        output_str = start_year + "年" + start_month + "月 - " + end_year + "年" + end_month + "月 共" + duration_year + "年" + duration_month+ "月"
      else:
        output_str = start_year + "年" + " - " + end_year + "年共" + duration_year + "年"
  else:
    if int(end_year) == datetime.datetime.now().year and int(end_month) == datetime.datetime.now().month:
      if has_month_info == True:
        output_str = start_year + "年" + start_month + "月 - " + end_year + "年" + end_month + "月(目前) 共" + duration_month + "月"
      else:
        output_str = start_year + "年" + " - " + end_year + "年(目前) 共" + duration_year + "年"
    else:
      if has_month_info == True:
        output_str = start_year + "年" + start_month + "月 - " + end_year + "年" + end_month + "月 共" + duration_month + "月"
      else:
        output_str = start_year + "年" + " - " + end_year + "年共" + duration_year + "年"
  f_w.write(output_str)
  f_w.write('\n')


def caculate_company_duration(info_tuple_list):
  #紀錄在該間公司工作時長
  company_duration = {}
  for i in range(len(info_tuple_list)):
    CompanyName = info_tuple_list[i][1]
    start_time_value = int(info_tuple_list[i][5]) * 12 + int(info_tuple_list[i][6])
    end_time_value = info_tuple_list[i][0]
    duration_year = info_tuple_list[i][9]
    duration_month = info_tuple_list[i][10]
    try:
      min_time_value = company_duration[CompanyName][0]
      if end_time_value == min_time_value:
        company_duration[CompanyName][1] += duration_year * 12 + duration_month - 1
        company_duration[CompanyName][0] = start_time_value
      elif end_time_value < min_time_value:
        company_duration[CompanyName][1] += duration_year * 12 + duration_month
        company_duration[CompanyName][0] = start_time_value
      else:
        if start_time_value < min_time_value:
          company_duration[CompanyName][1] += duration_year * 12 + duration_month - (end_time_value - min_time_value) - 1
          company_duration[CompanyName][0] = start_time_value
    except:
      #公司名稱還未被紀錄
      company_duration[CompanyName] = [start_time_value, duration_year * 12 + duration_month]
  return company_duration

def find_school_name_by_fsd_school(main_info):
  pattern = r'fsd_school:[0-9]*?","name":.*?,"'
  raw_school_info = re.findall(pattern, main_info)[0]
  schoolName = get_info(raw_school_info, '"name"')
  return schoolName

def get_education_info(main_info, sample_raw, education_info_list):
  schoolName = get_info(sample_raw, '"schoolName"')
  activities = get_info(sample_raw, '"activities"')
  description = get_info(sample_raw, '"description"')
  if schoolName == "null":
    schoolName = find_school_name_by_fsd_school(main_info)
  degreeName = get_info(sample_raw, '"degreeName"')
  if degreeName == "null":
    degreeName = ""
  fieldOfStudy = get_info(sample_raw, '"fieldOfStudy"')
  if fieldOfStudy == "null":
    fieldOfStudy = ""
  #獲取入學與畢業年份
  try:
    start_date(sample_raw)
  except Exception as e:
    start_year_school = str(e)
  try:
    #如果還沒畢業
    year, month = end_date(sample_raw)
    end_year_school = year
  except Exception as e:
    end_year_school = str(e)
  school_info_string = schoolName + "," + degreeName + "," + fieldOfStudy
  education_info_list.append((end_year_school, start_year_school, school_info_string, activities, description))
  return schoolName

def print_education_info(education_info_list):
  for i in range(len(education_info_list)):
    end_year_school, start_year_school, school_info_string, activities, description = education_info_list[i]
    f_w.write(school_info_string)
    f_w.write('\n')
    f_w.write("就學期間:" + start_year_school + "年 - " + end_year_school + "年")
    f_w.write('\n')
    if activities != "null":
      f_w.write("活動和社團:\n" + activities)
      f_w.write('\n')
    if description != "null":
      f_w.write(description)
      f_w.write('\n')
    f_w.write("\n")

def get_experience_education_process(main_info, name_code):
  set_f_w(name_code)
  pattern = r'Range":{"start":.*?"date'
  working_experience_and_education_list_raw = re.findall(pattern, main_info)


  #記錄開始工作時間看有沒有重複抓取資料與排時間序使用
  start_time_value_list = []
  #紀錄結束工作時間
  end_time_value_list = []
  #紀錄工作名稱
  title_list = []
  #記錄資訊
  info_tuple_list = []
  #紀錄教育背景的sample_raw
  education_sample_raw_list = []
  schoolName_list = []
  for i in range(len(working_experience_and_education_list_raw)):
    sample_raw = working_experience_and_education_list_raw[i]
    try:
      start_year, start_month = start_date(sample_raw)
    except Exception as e:
      education_sample_raw_list.append(sample_raw)
      continue
    end_year, end_month = end_date(sample_raw)
    duration_year, duration_month = calculate_duration(start_year, start_month, end_year, end_month)
    title = get_info(sample_raw, '"title"')
    companyName = get_info(sample_raw, '"companyName"')
    locationName = get_info(sample_raw, '"locationName"')
    description = get_info(sample_raw, '"description"')
    start_time_value = int(start_year) * 12 + int(start_month)
    end_time_value = int(end_year) * 12 + int(end_month)
    if title == None:
      continue
    elif start_time_value in start_time_value_list:
      index_list = list(locate(start_time_value_list, lambda x: x == start_time_value))
      duplicate = False
      for index in range(len(index_list)):
        if end_time_value == end_time_value_list[index] and title == title_list[index]:
          duplicate = True
          continue
        else:
          start_time_value_list.append(start_time_value)
          end_time_value_list.append(end_time_value)
          title_list.append(title)
      if duplicate == True:
        continue
    else:
      start_time_value_list.append(start_time_value)
      end_time_value_list.append(end_time_value)
      title_list.append(title)
    info_tuple = (end_time_value, companyName, title, locationName, description, start_year, start_month, end_year, end_month, duration_year, duration_month, start_time_value)
    info_tuple_list.append(info_tuple)

  info_tuple_list.sort(key=itemgetter(0, -1), reverse = True)
  company_duration = caculate_company_duration(info_tuple_list)
  f_w.write(" " * ((50 - len("$Experience$")) // 2) + "$Experience$")
  f_w.write('\n')
  latest_companyName = ""
  for i in range(len(info_tuple_list)):
    end_time_value, companyName, title, locationName, description, start_year, start_month, end_year, end_month, duration_year, duration_month, start_time_value = info_tuple_list[i]
    if companyName != latest_companyName:
      latest_companyName = companyName
      f_w.write('*' * 50)
      f_w.write('\n')
      if company_duration[latest_companyName][1] // 12 != 0:
        f_w.write("在" + companyName + "工作了" + str(company_duration[latest_companyName][1] // 12) + "年" + str(company_duration[latest_companyName][1] % 12) + "個月")
        f_w.write('\n')
      else:
        f_w.write("在" + companyName + "工作了" + str(company_duration[latest_companyName][1] % 12) + "個月")
        f_w.write('\n')
      f_w.write('*' * 50)
      f_w.write('\n')
    show_info(companyName, title, locationName, description, start_year, start_month, end_year, end_month, duration_year, duration_month)
  f_w.write(" " * ((50 - len("$Education$")) // 2) + "$Education$")
  f_w.write('\n')
  f_w.write("*" * 50)
  f_w.write('\n')
  education_info_list = []
  for i in range(len(education_sample_raw_list)):
    schoolName = get_education_info(main_info, education_sample_raw_list[i], education_info_list)
    schoolName_list.append(schoolName)
  education_info_list.sort(key=itemgetter(0,1), reverse = True)
  print_education_info(education_info_list)

  #最後回傳最高學歷與現今公司
  try:
    return schoolName_list[0], info_tuple_list[0][1]
  except:
    try:
      return schoolName_list[0], None
    except:
      try:
        return None, info_tuple_list[0][1]
      except:
        return None, None

def print_bio(firstName, lastName, premium_bool, headline, locationName, open_to_work_info, total_url, present_companyName, highest_schoolName, summary, url):
  f_w.write(firstName + " " + lastName + "(" + premium_bool + "premium會員)")
  f_w.write('\n')
  if headline != "null":
    f_w.write(headline)
    f_w.write('\n')
  if locationName != "null":
    f_w.write(locationName)
    f_w.write('\n')
  f_w.write(open_to_work_info)
  f_w.write('\n')
  f_w.write("個人網址:" + url)
  f_w.write('\n')
  f_w.write("圖片網址:" + total_url)
  f_w.write('\n')
  if present_companyName != None:
    f_w.write("現今公司:" + present_companyName)
    f_w.write('\n')
  if highest_schoolName != None:
    f_w.write("教育背景:" + highest_schoolName)
    f_w.write('\n')
  if summary != "null":
    f_w.write("關於:\n" + summary)
    f_w.write('\n')

def get_bio_process(name_code, highest_schoolName, present_companyName, main_info):
  url = "https://www.linkedin.com/in/" + name_code
  pattern = name_code + r'.*'
  bio_raw = re.findall(pattern, main_info)[0]
  profile_picture_pattern = r'"profilePicture":.*?"}]'
  profile_picture_zone_raw = re.findall(profile_picture_pattern, bio_raw)[0]
  try:
    rootUrl = get_info(profile_picture_zone_raw, '"rootUrl"')
    fileIdentifyingUrlPathSegment_800 = "800" + get_info(profile_picture_zone_raw, '"fileIdentifyingUrlPathSegment":"8').replace(";", "&")
    #linkedin的圖片網址有效期，過段時間要重爬，或是直接將圖片download下來
    total_url = rootUrl + fileIdentifyingUrlPathSegment_800
  except:
    total_url = "此會員沒有大頭照喔"
  firstName = get_info(bio_raw, '"firstName"')
  lastName = get_info(bio_raw, '"lastName"')
  premium_bool = get_info(bio_raw, '"premium"')
  if premium_bool == "als":
    premium_bool = "不是"
  elif premium_bool == "ru":
    premium_bool = "是"
  summary = get_info(bio_raw, '"summary"')
  open_to_work_bool = get_info(bio_raw, '"frameType"')
  if open_to_work_bool == "OPEN_TO_WORK":
    open_to_work_info = "他(她)準備好開始工作了"
  else:
    open_to_work_info = "他(她)還沒準備好開始工作"
  headline = get_info(bio_raw, '"headline"')
  locationName = get_info(bio_raw, '"locationName"')
  f_w.write(" " * ((50 - len("$Bio section$")) // 2) + "$Bio section$")
  f_w.write('\n')
  f_w.write("*" * 50)
  f_w.write('\n')
  print_bio(firstName, lastName, premium_bool, headline, locationName, open_to_work_info, total_url, present_companyName, highest_schoolName, summary, url)
  f_w.write('$' * 50)
  f_w.close()

if __name__ == '__main__':
  name_code_list = ["andrea-campbell-69911b11", "jessica-baldini-9b053217", "teresa-parker-8a4ab248", "chad-stafford-333202a", "olivia-mcfadin-04945a144" \
  , "cory-baker-308762b9", "tanjulan-major-8b52137", "kayln-williams-49a35245", "jason-rogers-a57859a", "josh-fox-80552666"]
  for i in range(len(name_code_list)):
    src = "./test" + str(i+1) + ".txt"
    highest_schoolName, present_companyName = get_experience_education_process(src)
    get_bio_process(name_code_list[i], highest_schoolName, present_companyName, src)










