import config

probID = "123"
uploadTime = "20:11:25"
subjectFileName = config.subjectFileName.replace("[probID]", probID).replace(
    "[uploadTime]", uploadTime
)

print(subjectFileName)
